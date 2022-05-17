import pandas as pd
import os
from db import DB
import logging
from redisUtil import TimeStamp
from filterPriceSpread import FilterPriceSpread
from tightMinMax import TightMinMax
from util import Util
from environ import EnvFile


class FilterSupplyDemandSimple:
    def __init__(self, marketOpenAt=None):
        self.marketOpenAt = TimeStamp.getMarketOpenTimestamp(
        ) if marketOpenAt is None else marketOpenAt
        self.minMaxRangePercent = 0.08
        self.minMaxNearPercent = 0.02

    def Run(self, symbol: str, dataf: pd.DataFrame, close: float) -> bool:
        try:
            df = dataf[dataf['Date'] >= self.marketOpenAt]
            if len(df) <= 3:
                return False
            close = df.iloc[0]
            iMax = df['High'].idxmax()
            iMin = df['Low'].idxmin()
            high = df.iloc[iMax]['High']
            low = df.iloc[iMin]['Low']
            if FilterPriceSpread.IsEnoughSpread(df, spread=0.04):
                if iMax > 2 and FilterPriceSpread.IsNearPrice(high, close, self.minMaxNearPercent):
                    return True
                if iMin > 2 and FilterPriceSpread.IsNearPrice(low, close, self.minMaxNearPercent):
                    return True
            return False
        except Exception as ex:
            logging.error(f'FilterDailySupplyDemandZone {symbol} - {ex}')
            return False

class FilterDailySupplyDemandZone:
    def __init__(self):
        self.fMinmax = TightMinMax(tightMinMaxN=3)
        self.minMaxNearPercent = 0.03
        self.takeoffSlope = float(EnvFile.Get('FILTER_SUPPLY_DEMAND_TAKEOFF_SLOPE', '0.06'))

    def IsPrerequisite(self, dataf: pd.DataFrame, close: float) -> bool:
        if len(dataf) <= 5:
            return False
        if FilterPriceSpread.IsEnoughSpread(dataf, self.minMaxRangePercent):
            return True
        return False

    def getMinmax(self, df: pd.DataFrame) -> dict:
        return Util.GetHighestLowestDf(df, 'High', 'Low');
        # iMax = df['High'].idxmax()
        # iMin = df['Low'].idxmin()
        # high = df.iloc[iMax]['High']
        # low = df.iloc[iMin]['Low']
        # return high, low

    def getMinmaxOnClose(self, df: pd.DataFrame) -> dict:
        high = None
        low = None
        for idx, row in df.iterrows():
            value = row['Close']
            if high is None:
                high = value
            if low is None:
                low = value
            if high < value:
                high = value
            if low > value:
                low = value
        return high, low

    def beforeAndAfterSlope(self, df: pd.DataFrame, close: float) -> pd.DataFrame:
        lastRow = None
        takeOffSlopes = []
        for idx, row in df.iterrows():
            if not lastRow is None:
                slope = (row['Close'] - lastRow['Close']) / (row['x'] - lastRow['x'])
                standardSlope = slope * Util.SlopeOfPrice(close)
                takeOffSlopes.append(abs(standardSlope))
            lastRow = row
        if len(df) > 0:
            takeOffSlopes.append(0)
        df = df.assign(Takeoff = takeOffSlopes)
        return df

    def firstKeyPoints(self, dataf: pd.DataFrame) -> list:
        df = dataf.reset_index()
        dataPoints = []
        try:
            for idx, row in df.iterrows():
                key = row['Close']
                takeoff = row['Takeoff']
                high, low = self.getMinmaxOnClose(df[idx+1:])
                if high is None or low is None:
                    dataPoints.append({'Close': key, 'Date': row['Date'], 'Takeoff': takeoff})
                if (high * 1.02) >= key >= (low * 0.98):
                    pass
                else:
                    dataPoints.append({'Close': key, 'Date': row['Date'], 'Takeoff': takeoff})
        except Exception as e:
            logging.error(f'firstKeyPoints {e}')
        return dataPoints
    
    def priceCount(self, close:float, df:pd.DataFrame, nearPercent:float) -> bool:
        for idx, row in df.iterrows():
            if FilterPriceSpread.IsNearPrice(row.Close, close, nearPercent):
                return True
        return False
    
    def matchHighLowKeyPoints(self, keypoints: pd.DataFrame, close: float, nearPercent: float) -> bool:
        highIdx, lowIdx = Util.GetHighestLowestIndexDf(keypoints, 'Close', 'Close')
        peakPoint = keypoints.iloc[highIdx] if highIdx > lowIdx else keypoints.iloc[lowIdx]
        if FilterPriceSpread.IsNearPrice(peakPoint.Close, close, nearPercent):
            return True

    def Run(self, symbol: str, df: pd.DataFrame, close: float) -> bool:
        try:
            close = df.iloc[0]['Close']
            if len(df) <= 5:
                return False
            if not FilterPriceSpread.IsEnoughSpread(df, self.minMaxRangePercent):
                return False
            isPtMin, keypoints = self.fMinmax.Run(df, isRemoveRepeatMinMaxOnly=True)
            if len(keypoints) < 2:
                return False
            if not self.matchHighLowKeyPoints(keypoints, close, self.minMaxNearPercent):
                return False
            
            return True
        except Exception as ex:
            logging.error(f'FilterDailySupplyDemandZone {symbol} - {ex}')
            return False

if __name__ == '__main__':
    one = FilterDailySupplyDemandZone()
    result = one.Run('FNV', 164.40)
    print(result)

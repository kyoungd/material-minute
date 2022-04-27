import pandas as pd
import os
from db import DB
import logging
from redisUtil import TimeStamp
from filterPriceSpread import FilterPriceSpread
from tightMinMax import TightMinMax
from util import Util

class FilterDailySupplyDemandZone:
    def __init__(self):
        self.fMinmax = TightMinMax(tightMinMaxN=3)
        self.minMaxNearPercent = 0.03
        self.takeoffSlope = 1

    def IsPrerequisite(self, dataf: pd.DataFrame, close: float) -> bool:
        if len(dataf) <= 5:
            return False
        if FilterPriceSpread.IsEnoughSpread(dataf, 0.04):
            return True
        return False

    def getMinmax(self, df: pd.DataFrame) -> dict:
        iMax = df['High'].idxmax()
        iMin = df['Low'].idxmin()
        high = df.iloc[iMax]['High']
        low = df.iloc[iMin]['Low']
        return high, low

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
            else:
                takeOffSlopes.append(0)
            lastRow = row
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
                    dataPoints.append({'Close': key, 'Takeoff': takeoff})
                if (high * 1.02) >= key >= (low * 0.98):
                    pass
                else:
                    dataPoints.append({'Close': key, 'Takeoff': takeoff})
        except Exception as e:
            logging.error(f'firstKeyPoints {e}')
        return dataPoints
    
    def Run(self, symbol: str, df: pd.DataFrame, close: float) -> bool:
        try:
            if not self.IsPrerequisite(df, close):
                return False
            isPtMin, keypoints = self.fMinmax.Run(df, isRemoveRepeatMinMaxOnly=True)
            keypoints:pd.DataFrame = self.beforeAndAfterSlope(keypoints, close)
            firstkeys:list = self.firstKeyPoints(keypoints[::-1])
            for row in firstkeys:
                if FilterPriceSpread.IsNearPrice(row['Close'], close, self.minMaxNearPercent) and row['Takeoff'] >= self.takeoffSlope:
                    return True
            return False
        except Exception as ex:
            logging.error(f'FilterDailySupplyDemandZone {symbol} - {ex}')
            return False

if __name__ == '__main__':
    one = FilterDailySupplyDemandZone()
    result = one.Run('FNV', 164.40)
    print(result)

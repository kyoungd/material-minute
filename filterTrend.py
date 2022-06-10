import os
import talib
from environ import EnvFile
from tightMinMax import TightMinMax
import pandas as pd
import os
import logging
from redisUtil import TimeStamp
from util import Util

class trendMinMax:
    def __init__(self, minmaxs: pd.DataFrame, isFirstMin: bool, close: float):
        self.df = minmaxs
        self.isFirstMin = isFirstMin
        self.close = close
        self.minimumTrend = float(EnvFile.Get("FILTER_TREND_COUNT", '1.5'))
        self.minimumDelta = float(EnvFile.Get("FILTER_TREND_DELTA", '0.03'))

    def isIncludeTodayClose(self, todayClose: float, df: pd.DataFrame):
        pivot1 = df.iloc[0]['Close']
        pivot2 = df.iloc[1]['Close']
        pivot3 = df.iloc[2]['Close']
        if todayClose == pivot1:  # same data point as last pivot.  ignore.
            return False
        if (pivot1 > pivot3):  # trending up
            if (pivot1 > pivot2):  # pivot1 is max
                return todayClose < pivot2
            else:  # pivot1 is min
                return False
        else:  # trending down
            if (pivot1 > pivot2):  # pivot1 is max
                return False
            else:  # pivot1 is min
                return todayClose > pivot2
        return False

    def getDirections(self, df: pd.DataFrame, isFirstMin: bool, minDelta: float) -> list:
        try:
            directions = []
            if len(df.index) < 3:
                return []
            for ix, row in df.iterrows():
                if ix >= 2:
                    thisValue = row['Close']
                    lastValue = df.iloc[ix - 2]['Close']
                    if thisValue > lastValue:
                        directions.append('up')
                    else:
                        directions.append('down')
            return directions
        except Exception as e:
            logging.error(f'trendMinMax.getDirections: {e}')
            return []

    def trendingLoops(self, directions: list, isFirstMin: bool, close: float, minDelta: float) -> bool:
        try:
            dir1 = directions[0]
            dir2 = dir1
            count1 = 0
            count2 = 0
            isFirstTrend = True
            for dir1 in directions:
                if dir1 == dir2:
                    if isFirstTrend:
                        count1 += 0.5
                    else:
                        count2 += 0.5
                else:
                    if isFirstTrend:
                        isFirstTrend = False
                        count2 += 0.5
                    else:
                        return count1, count2
                dir2 = dir1
            return count1, count2
        except Exception as e:
            logging.error(f'trendMinMax.trendingLoops: {e}')
            return 0, 0

    def Run(self) -> set:
        directions = self.getDirections(
            self.df, self.isFirstMin, self.minimumDelta)
        if len(directions) <= 0:
            return 0, 0
        trend1, trend2 = self.trendingLoops(
            directions, self.isFirstMin, self.close, self.minimumDelta)
        if self.isIncludeTodayClose(self.close, self.df):
            return 0.5, trend1
        else:
            return trend1, trend2

class FilterTrends:
    def __init__(self):
        self.minimumReversePeaks:float = float(EnvFile.Get("FILTER_TREND_REVERSE_COUNT", '1'))
        self.maximumReversePeaks:float = float(EnvFile.Get("FILTER_TREND_REVERSE_COUNT_MAX", '2.0'))
        self.minimumTrendPeaks:float = float(EnvFile.Get("FILTER_TREND_MINIMUM_PEAKS", '0.5'))
        self.marketOpenAt = TimeStamp.getMarketOpenTimestamp()

    def getEma(self, df: pd.DataFrame, lookback: int = None) -> pd.DataFrame:
        lookback = 9 if lookback is None else lookback
        df1 = df[::-1]
        df1 = df1.reset_index()
        closesMean = talib.EMA(df1.Close, lookback)
        df2 = df1.assign(ema9=closesMean)
        df2 = df2[::-1]
        df2 = df2.reset_index()
        return df2

    def isEma9Verified(self, df: pd.DataFrame, idxA: int, idxB: int) -> bool:
        isMovingUp = True if df.iloc[idxA].Close < df.iloc[idxB].Close else False
        for idx in range(0, idxB):
            close = df.iloc[idx].Close
            ema9 = df.iloc[idx].ema9
            if isMovingUp and close < ema9:
                return False
            if not isMovingUp and close > ema9:
                return False
        return True

    def isNewTrend(self, df: pd.DataFrame, isFirstMinimum: bool, close: float) -> list:
        trend = trendMinMax(df, isFirstMinimum, close)
        trendPeaks, reversePeaks = trend.Run()
        if trendPeaks < self.minimumTrendPeaks:
            return False
        newPeaks = trendPeaks if reversePeaks <= 0 else reversePeaks
        if newPeaks > self.maximumReversePeaks:
            return False
        if newPeaks < self.minimumReversePeaks:
            return False
        return True

    def isEma9Ok(self, df:pd.DataFrame, indexA: int, indexB: int) -> bool:
        ema9 = self.getEma(df)
        if self.isEma9Verified(ema9, indexA, indexB):
            return True
        return False
        
    def isFirstPointMin(self, dfAllLength: int, dfMarketOpen: int, isFirstMinimum: bool)-> bool:
        if (dfAllLength - dfMarketOpen) % 2 == 0:
            return isFirstMinimum
        else:
            return not isFirstMinimum
    
    def Run(self, symbol:str, dfDaily:pd.DataFrame, dfMinMax:pd.DataFrame = None, isFirstMinimum: bool = None) -> bool:
        try:
            close = dfDaily['Close'][0]  # last close price
            minMax = TightMinMax()
            isFirstMinimum, df = minMax.Run(symbol) if dfMinMax is None else (isFirstMinimum, dfMinMax)  # calculate local min
            if df is None:
                return False
            if not self.isNewTrend(df, isFirstMinimum, close):
                return False
            if not self.isEma9Ok(df, df.iloc[0].x, df.iloc[1].x):
                return False
            return True
        except Exception as e:
            logging.error(f'FilterTrends.Run: {symbol} {e}')
            print(e)
            return False

    def RunNew(self, symbol:str, dfDaily:pd.DataFrame, dfMinMax:pd.DataFrame = None, isFirstMinimum: bool = None) -> bool:
        try:
            close = dfDaily['Close'][0]  # last close price
            minMax = TightMinMax()
            isFirstMinimum, df = minMax.Run(symbol) if dfMinMax is None else (isFirstMinimum, dfMinMax)  # calculate local min
            if df is not None and (len(df.index) > 2):
                if self.isNewTrend(df, isFirstMinimum, close):
                    dfDaily = Util.GetEma(dfDaily, 'ema9', 9)
                    indexA = df.iloc[0].index
                    indexB = df.iloc[1].index
                    if not Util.IsAboveEma(dfDaily, 0, indexB, 'ema9'):
                        return False
                    if len(dfDaily) < (26 + indexB):
                        return True
                    dfDaily = Util.GetEma(dfDaily, 'ema12', 12)
                    dfDaily = Util.GetEma(dfDaily, 'ema26', 26)
                    if not Util.IsAboveOtherEma(dfDaily, indexA, indexB, 'ema12', 'ema26'):
                        return False
                    return True
            return False
        except Exception as e:
            logging.error(f'FilterTrends.Run: {symbol} {e}')
            print(e)
        return False

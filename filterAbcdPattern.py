import pandas as pd
from sortedcollections import IndexableDict
import talib
from db import DB
import logging
from redisUtil import TimeStamp
from tightMinMax import TightMinMax
from util import Util

class FilterAbcdPattern:
    def __init__(self):
        self.fMinmax = TightMinMax(tightMinMaxN=2)
        self.isFirstMin = None
        self.minMaxRangePercent = 0.03
        self.minMaxNearPercent = 0.01
 
    def IsAbcdPattern(self, A:float, B: float, C: float, close) -> bool:
        if not ((A > C > B) or (A < C < B)):
            return False
        if not Util.IsPriceSpread(A, B, self.minMaxRangePercent):
            return False
        if not Util.IsNearPrice(B, close, self.minMaxNearPercent):
            return False
        return True

    def getEma(self, df: pd.DataFrame, lookback: int = None) -> pd.DataFrame:
        lookback = 9 if lookback is None else lookback
        df1 = df[::-1]
        df1 = df1.reset_index()
        closesMean = talib.EMA(df1.Close, lookback)
        df2 = df1.assign(ema9=closesMean)
        df2 = df2[::-1]
        df2 = df2.reset_index()
        return df2
        
    def isEma9Verified(self, df: pd.DataFrame, idxA:int, idxB:int, idxC:int) -> bool:
        isMovingUp = True if df.iloc[idxA].Close < df.iloc[idxB].Close else False
        for idx in range(0, idxB):
            close = df.iloc[idx].Close
            ema9 = df.iloc[idx].ema9
            if isMovingUp and close < ema9:
                return False
            if not isMovingUp and close > ema9:
                return False
        return True

    def getChopinessIndex(self, df: pd.DataFrame) -> pd.DataFrame:
        df1 = df[::-1]
        df1.reset_index()
        df1['ChopinessIndex'] = Util.ChoppinessIndex(df['High'], df['Low'], df['Close'])
        df2 = df1[::-1]
        df2.reset_index()
        return df2
                        
    def isTrending(self, df: pd.DataFrame, idxA, idxB, idxC) -> bool:
        for idx in range(idxB, idxC):
            if not Util.IsTrending(df.iloc[idx].ChoppinessIndex):
                return False
        return True

    def getMacdData(self, df: pd.DataFrame) -> pd.Series:
        df1 = df[::-1].reset_index()
        close = df1.Close
        macd, macdsignal, macdhist = talib.MACD(
            close, fastperiod=12, slowperiod=26, signalperiod=9)
        return macdhist

    def isMacdHistogramSync(self, macdHist:pd.Series, ixA:int, ixB:int, ixC:int, isPositive:bool) -> bool:
        dfMacd = macdHist[::-1]
        dfMacd.reset_index()
        lastHist = dfMacd.iloc[ixA]
        ixEnd = int(round(ixB + ixC / 2))
        for ix in range(ixB, len(macdHist)):
            if not Util.IsSameSign(dfMacd.iloc[ix], lastHist):
                return False
        return True

    def abcPatternResult(self, df: pd.DataFrame, dfMinMax: pd.DataFrame, ixA: int, ixB: int, ixC: int, close:float):
        pointA = dfMinMax.iloc[ixA]
        pointB = dfMinMax.iloc[ixB]
        pointC = dfMinMax.iloc[ixC]
        if self.IsAbcdPattern(pointA.Close, pointB.Close, pointC.Close, close):
            ema9 = self.getEma(df)
            if self.isEma9Verified(ema9, pointA.x, pointB.x, pointC.x):
                return True
        return False

    def Run(self, symbol:str, df: pd.DataFrame, close: float) -> bool:
        try:
            close = df.iloc[0]['Close']
            isFirstMin, dfMinMax= self.fMinmax.Run(df)
            if len(dfMinMax) < 3:
                return False
            if self.abcPatternResult(df, dfMinMax, 2, 1, 0, close):
                return True
            if len(dfMinMax) < 4:
                return False
            if self.abcPatternResult(df, dfMinMax, 3, 2, 1, close):
                return True
            if len(dfMinMax) < 5:
                return False
            if self.abcPatternResult(df, dfMinMax, 4, 1, 0, close):
                return True
            if self.abcPatternResult(df, dfMinMax, 4, 3, 0, close):
                return True
            return False
        except Exception as ex:
            logging.error(f'FilterAbcdPattern {symbol} - {ex}')
            return False


def readFromDb(db, symbol):
    query = """SELECT keylevels, is_first_key_level_min FROM public.market_data WHERE symbol=%s AND timeframe=%s AND NOT is_deleted"""
    params = (symbol, '1Day')
    isOk, results = db.SelectQuery(query, params)
    if isOk:
        row = results[0]
        data = row[0]
        isFirstKeyLevelMin = row[1]
        return isFirstKeyLevelMin, data
    return False, None

if __name__ == '__main__':
    db = DB()
    isFirstMin, df = readFromDb(db, 'AAPL')
    one = FilterAbcdPattern()
    result = one.Run('AAPL', df)
    print(result)

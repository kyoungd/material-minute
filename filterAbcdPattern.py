import pandas as pd
import talib
from db import DB
import logging
from redisUtil import TimeStamp
from tightMinMax import TightMinMax
from filterPriceSpread import FilterPriceSpread
from util import Util

class FilterAbcdPattern:
    def __init__(self):
        self.fMinmax = TightMinMax(tightMinMaxN=4)
        self.isFirstMin = None
 
    def IsAbcdPattern(self, A:float, B: float, C: float, close) -> bool:
        if (B > A > C) or (B < A < C):
            if FilterPriceSpread.IsNearPrice(B, close):
                return True
        return False

    def getMacdData(self, df: pd.DataFrame) -> pd.Series:
        df1 = df[::-1].reset_index()
        close = df1.Close
        macd, macdsignal, macdhist = talib.MACD(
            close, fastperiod=12, slowperiod=26, signalperiod=9)
        return macdhist

    def isMacdHistogramSync(self, macdHist:pd.Series, ixA:int, ixB:int, ixC:int) -> bool:
        dfMacd = macdHist[::-1]
        dfMacd.reset_index()
        lastHist = dfMacd.iloc[ixA]
        ixEnd = int(round(ixB + ixC / 2))
        for ix in range(ixA, ixEnd):
            if not Util.IsSameSign(dfMacd.iloc[ix], lastHist):
                return False
        return True
        
    def Run(self, symbol:str, dataf: pd.DataFrame, close: float) -> bool:
        try:
            isFirstMin, df = self.fMinmax.Run(dataf)
            if len(df) >= 3 and self.IsAbcdPattern(df.iloc[0]['Close'], df.iloc[1]['Close'], df.iloc[2]['Close'], close):
                df1 = self.getMacdData(dataf[::-1])
                if self.isMacdHistogramSync(df1, df.iloc[0]['x'], df.iloc[1]['x'], df.iloc[2]['x']):
                    return True
            if len(df) >= 5 and self.IsAbcdPattern(df.iloc[0]['Close'], df.iloc[1]['Close'], df.iloc[4]['Close'], close):
                df1 = self.getMacdData(dataf[::-1])
                if self.isMacdHistogramSync(df1, df.iloc[0]['x'], df.iloc[1]['x'], df.iloc[4]['x']):
                    return True
            if len(df) >= 5 and self.IsAbcdPattern(df.iloc[0]['Close'], df.iloc[3]['Close'], df.iloc[4]['Close'], close):
                df1 = self.getMacdData(dataf[::-1])
                if self.isMacdHistogramMSync(df1, df.iloc[0]['x'], df.iloc[3]['x'], df.iloc[4]['x']):
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

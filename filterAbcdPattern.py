import pandas as pd
import os
from db import DB
import logging
from redisUtil import TimeStamp
from tightMinMax import TightMinMax
from filterPriceSpread import FilterPriceSpread

class FilterAbcdPattern:
    def __init__(self):
        self.fMinmax = TightMinMax(tightMinMaxN=4)
        self.isFirstMin = None
 
    def IsAbcdPattern(self, A:float, B: float, C: float, close) -> bool:
        if (B > C > A) or (B < C < A):
            if FilterPriceSpread.IsNearPrice(B, close):
                return True
        return False

    def Run(self, symbol:str, dataf: pd.DataFrame, close: float) -> bool:
        try:
            isFirstMin, df = self.fMinmax.Run(dataf)
            if len(df) >= 3 and self.IsAbcdPattern(df.iloc[0][1], df.iloc[1][1], df.iloc[2][1], close):
                return True
            if len(df) >= 5 and self.IsAbcdPattern(df.iloc[0][1], df.iloc[1][1], df.iloc[4][1], close):
                return True
            if len(df) >= 5 and self.IsAbcdPattern(df.iloc[0][1], df.iloc[3][1], df.iloc[4][1], close):
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

import pandas as pd
import os
from db import DB
import logging
from redisHash import KeyLevelsStack
from redisUtil import TimeStamp
from filterPriceSpread import FilterPriceSpread
from tightMinMax import TightMinMax
from util import Util
from environ import EnvFile

class FilterKeyLevels:
    def __init__(self):
        self.fMinmax = TightMinMax(tightMinMaxN=3)
        self.minMaxRangePercent = 0.08
        self.minMaxNearPercent = 0.03
        self.stack = KeyLevelsStack()
    
    def isNearKeyLevel(self, price: float, keylevels:list, nearPercent:float) -> bool:
        nearPercent = self.minMaxNearPercent if nearPercent is None else nearPercent
        for keylevel in keylevels:
            if Util.IsNearPrice(price, keylevel.Close, nearPercent):
                return True
        return False

    def Run(self, symbol: str, df: pd.DataFrame, dfMinMax: pd.DataFrame = None, keylevels: list = None) -> bool:
        try:
            close = df.iloc[0]['Close']
            if len(df) <= 5:
                return False
            if not FilterPriceSpread.IsEnoughSpread(df, self.minMaxRangePercent):
                return False
            _, minmax = self.fMinmax.Run(df) if dfMinMax is None else (False, dfMinMax)
            minmax1 = None if len(minmax) < 1 else minmax.iloc[0]
            minmax2 = None if len(minmax) < 2 else minmax.iloc[1]
            keylevels = self.stack.Get(
                symbol) if keylevels is None else keylevels
            if len(keylevels) > 0:
                for kl in keylevels:
                    if Util.IsNearPrice(close, kl['Close'], self.minMaxNearPercent):
                        if minmax1 is not None:
                            if Util.IsNearPrice(minmax1.Close, kl['Close'], self.minMaxNearPercent):
                                if Util.IsNearPrice(close, minmax1.Close, self.minMaxNearPercent):
                                    return True
                        if minmax2 is not None:
                            if Util.IsNearPrice(minmax2.Close, kl['Close'], self.minMaxNearPercent):
                                if Util.IsNearPrice(close, minmax2.Close, self.minMaxNearPercent):
                                    return True

            return False
        except Exception as ex:
            logging.error(f'FilterDailySupplyDemandZone {symbol} - {ex}')
            return False


if __name__ == '__main__':
    one = FilterKeyLevels()
    result = one.Run('FNV', 164.40)
    print(result)

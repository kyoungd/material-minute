import pandas as pd
import logging
from util import Util

class UtilEma:
    def __init__(self, df:pd.DataFrame):
        self.df = df

    def SetEma(self, period:int):
        try:
            colName = f'ema{period}'
            if colName in self.df.columns:
                return
            self.df = Util.GetEma(self.df, emaName=colName, lookback=period)
        except Exception as e:
            logging.error(f'UtilEma.SetEma: {e}')

    def IsCloseOverEmaPeriod(self, period:int, indexA:int, indexB:int) -> bool:
        colName = f'ema{period}'
        isMovingUp = True if self.df.iloc[indexA].Close < self.df.iloc[indexB].Close else False
        for idx in range(indexA, indexB):
            close = self.df.iloc[idx].Close
            emaN = self.df.iloc[idx][colName]
            if isMovingUp and close < emaN:
                return False
            if not isMovingUp and close > emaN:
                return False
        return True

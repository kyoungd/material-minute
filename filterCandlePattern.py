import pandas as pd
import numpy as np
import pandas as pd
import numpy as np
import talib
import os
from datetime import date
import logging


class engulfingCandle:
    def __init__(self, df, minChangePercent, minChangeValue):
        data = df.loc[0:4]
        self.data = data[::-1]
        minCalcPrice = self.data.iloc[0].Close * minChangePercent
        self.minValue = minChangeValue if minCalcPrice < minChangeValue else minCalcPrice

    def CDLENGULFING(self, df):
        res = talib.CDLENGULFING(
            df.Open.values, df.High.values, df.Low.values, df.Close.values)
        return res

    def CDLENGULFING_MIN(self, df, result, minChange):
        for index, row in df.iterrows():
            if index > 0 and result[index] != 0:
                change = abs(df.Open[index] - df.Close[index-1])
                return True if change >= minChange else False
        return False

    def run(self):
        step1 = self.CDLENGULFING(self.data)
        result = self.CDLENGULFING_MIN(self.data, step1, self.minValue)
        return result


class starCandle:
    def __init__(self, symbol: str, df: pd.DataFrame):
        data = df.loc[0:5]
        self.data = data[::-1]
        self.symbol = symbol

    def CDLEVENINGDOJISTAR(self, df):
        o = df.Open
        h = df.High
        l = df.Low
        c = df.Close
        p = 0
        res = talib.CDLEVENINGDOJISTAR(o, h, l, c)
        return res

    def CDLEVENINGSTAR(self, df):
        o = df.Open
        h = df.High
        l = df.Low
        c = df.Close
        p = 0
        res = talib.CDLEVENINGSTAR(o, h, l, c)
        return res

    def CDLMORNINGDOJISTAR(self, df):
        o = df.Open
        h = df.High
        l = df.Low
        c = df.Close
        p = 0
        res = talib.CDLMORNINGDOJISTAR(o, h, l, c)
        return res

    def CDLMORNINGSTAR(self, df):
        o = df.Open
        h = df.High
        l = df.Low
        c = df.Close
        p = 0
        res = talib.CDLMORNINGSTAR(o, h, l, c)
        return res

    def run(self):
        try:
            print(self.data)
            step1 = self.CDLEVENINGDOJISTAR(self.data)
            step2 = self.CDLEVENINGSTAR(self.data)
            step3 = self.CDLMORNINGDOJISTAR(self.data)
            step4 = self.CDLMORNINGSTAR(self.data)
            return sum(step1) + sum(step2) + sum(step3) + sum(step4)
        except Exception as e:
            logging.error(
                f'filterCandlePattern.starPattern.run: {self.symbol} - {e}')
            return 0


class FilterCandlePattern:
    def __init__(self):
        self.minEngulfingCandleChangePercent = float(
            os.environ.get('MIN_ENGULFING_CANDLE_CHANGE_PERCENT', '0.03'))
        self.minEngulfingCandleChangevalue = float(
            os.environ.get('MIN_ENGULFING_CANDLE_CHANGE_VALUE', '0.2'))

    def Run(self, symbol, df:pd.DataFrame):
        try:
            filterEngulf = engulfingCandle(
                df, self.minEngulfingCandleChangePercent, self.minEngulfingCandleChangevalue)
            filterStar = starCandle(symbol, df)
            engulf = filterEngulf.run()
            star = filterStar.run()
            result = 1 if engulf > 0 else 0
            result = result + 2 if star > 0 else result
            return result
        except Exception as e:
            logging.error(f'filterCandlePattern.Run: {symbol} - {e}')
            print(f'filterCandlePattern.Run: {symbol} - {e}')
        return 0

if __name__ == '__main__':
    pass

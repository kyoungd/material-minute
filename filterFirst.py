import pandas as pd
import numpy as np
import pandas as pd
import numpy as np
import talib
import os
from datetime import date
import logging


class filterPriceVolume:
    def __init__(self):
        self.minPrice:float = float(
            os.environ.get('FIRST_FILTER_MIN_PRICE', '5'))
        self.minVolume:int = int(os.environ.get('FIRST_FILTER_MIN_VOLUME', '100000'))

    def filterPrice(self, close:float) -> bool:
        return close < self.minPrice

    def filterVolume(self, volume) -> bool:
        return volume < self.minVolume

class calculateATR:
    def __init__(self, barCount:int):
        self.atrTimeperiod = barCount

    def filterOn(self, tp):
        high = tp.High.to_numpy()
        low = tp.Low.to_numpy()
        close = tp.Close.to_numpy()
        output = talib.ATR(high[::-1], low[::-1], close[::-1], timeperiod=self.atrTimeperiod)
        output = output[np.logical_not(np.isnan(output))]
        end = len(output)
        start = end - self.atrTimeperiod
        start = 0 if start < 0 else start
        avgValue = np.mean(output[start:end])
        lastValue = output[-1]
        return avgValue, lastValue

    def Run(self, symbol:str, df: pd.DataFrame):
        try:
            _avg, _last = self.filterOn(df)
            return {'avg': _avg, 'last': _last, 'close': df['Close'][0]}
        except Exception as e:
            logging.error(f'filterAtr.calculateATR.Run: {symbol} - {e}')
            print(f'filterAtr.calculateATR.Run: {symbol} - {e}')
        return {'avg': 0, 'last': 0, 'close': 0}

class filterAtr:
    def __init__(self):
        self.atrFilterRate:float = float(os.environ.get('FIRST_FILTER_ATR_RATE', '5'))
        self.atrTimeperiod:int = int(os.environ.get(
            'FIRST_FILTER_ATR_PERIOD', '14'))
        self.filter = calculateATR(self.atrTimeperiod)

    def cleanUp(self, oneValue):
        if np.isnan(oneValue):
            return 0
        return round(oneValue, 2)

    def adjustedChangeValue (self, changeRate, close):
        if close < 10:
            change = changeRate * 10
        elif close < 20:
            change = changeRate * 8
        elif close < 40:
            change = changeRate * 6
        elif close < 60:
            change = changeRate * 4
        elif close < 80:
            change = changeRate * 2
        elif close < 100:
            change = changeRate * 1.5
        elif close < 200:
            change = changeRate
        elif close < 500:
            change = changeRate / 1.5
        else:
            change = changeRate / 2
        return change

    def Run(self, symbol:str, df: pd.DataFrame):
        try:
            result = self.filter.Run(symbol, df)
            changeRate = (result['avg'] / result['close']) * 100
            change = self.adjustedChangeValue(changeRate, result['close'])
            filterState = True if change < self.atrFilterRate else False
            return filterState
        except Exception as e:
            logging.error(f'filterAtr.FilterAtr.Run: {symbol} - {e}')
            print(f'filterAtr.FilterAtr.Run: {symbol} - {e}')
            return False

class FilterFirst:
    def __init__(self):
        self.pv = filterPriceVolume()
        self.atr = filterAtr()

    def IsFilter(self, symbol:str, df: pd.DataFrame):
        try:
            close = df.iloc[0]['Close']
            volume = df.iloc[0]['Volume']
            if self.pv.filterPrice(close) or self.pv.filterVolume(volume):
                return True
            if self.atr.Run(symbol, df):
                return True
            return False
        except Exception as e:
            logging.error(f'filterAtr.FirstFilter.Run: {symbol} - {e}')
            print(f'filterAtr.FirstFilter.Run: {symbol} - {e}')
            return False

if __name__ == '__main__':
    pass

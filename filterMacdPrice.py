import pandas as pd
import talib
import logging
from util import Util
from redisUtil import RedisTimeFrame


class FilterMacdPrice:
    def ___init__(self):
        pass

    def getMinimumPriceChange(self, timeframe):
        timePriceIntervals = {
            RedisTimeFrame.MIN2: 0.5,
            RedisTimeFrame.MIN5: 0.75,
            RedisTimeFrame.MIN15: 1.0
        }
        minPrice = timePriceIntervals.get(timeframe, None)
        timePercentIntervals = {
            RedisTimeFrame.MIN2: 0.2,
            RedisTimeFrame.MIN5: 0.25,
            RedisTimeFrame.MIN15: 0.3
        }
        minPercent = timePercentIntervals.get(timeframe, None)
        return minPrice, minPercent

    def firstAndSecondCrossover(self, hist: list) -> tuple:
        index1 = None
        index2 = None
        try:
            for i in range(len(hist) - 1, -1, -1):
                if not Util.IsSameSign(hist[i], hist[i - 1]) and (i > 0):
                    if index1 is None:
                        index1 = i
                    elif index1 is not None and index2 is None:
                        index2 = i
                        return index1, index2
        except Exception as e:
            logging.error(f'filterMacdPrice.firstAndSecondCrossover: {e}')
        return None, None
        
    def Run(self, symbol: str, df: pd.DataFrame, timeframe: str) -> bool:
        try:
            if len(df.index) < 27:
                return False
            dfDaily = df[::-1]
            dfDaily.reset_index(inplace=True)
            minPrice, minPercent = self.getMinimumPriceChange(timeframe)
            if minPrice is None or minPercent is None:
                logging.error(f"FilterMacdPrice.Run: {timeframe} is not supported")
                return False
            macd, signal, hist = talib.MACD(
                    dfDaily['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
            if Util.IsSameSign(hist.values[-1], hist.values[-2]) and Util.IsSameSign(hist.values[-2], hist.values[-3]):
                return False
            index1, index2 = self.firstAndSecondCrossover(hist.values)
            if index1 is None or index2 is None:
                return False
            price1 = dfDaily.iloc[index1].Close
            price2 = dfDaily.iloc[index2].Close
            delta = abs(abs(price1) - abs(price2))
            if delta < minPrice:
                return False
            if delta < (price1 + price2) / 2 * minPercent:
                return False
            return True
        except Exception as e:
            logging.error(f'filterMacdPrice.Run: {symbol} - {e}')
            print(f'filterMacdPrice.Run: {symbol} - {e}')
            return False

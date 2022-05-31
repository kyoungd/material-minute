import logging
from pubsubKeys import PUBSUB_KEYS
from redisPubsub import RedisPublisher, RedisSubscriber
from redisTimeseriesData import RealTimeBars
from redisUtil import RedisTimeFrame
import pandas as pd
from filterVolumeSpreadAnalysis import volumeSpreadAnalysis
from filterCandlePattern import FilterCandlePattern
from filterFirst import FilterFirst
from filterSupplyDemandZone import FilterDailySupplyDemandZone
from filterPriceSpread import FilterPriceSpread
from filterAbcdPattern import FilterAbcdPattern
from filterPivotPoint import FilterPivotPoint
from filterKeylevels import FilterKeyLevels
from tightMinMax import TightMinMax
from filterTrend import FilterTrends

class EventBarDataProcess:

    def __init__(self, pubKeyStack=None, pubTrade=None):
        # StoreStack: class to access the redis Stack.
        self.publisher = RedisPublisher(
            PUBSUB_KEYS.EVENT_BAR_STACK_ADD) if pubKeyStack is None else pubKeyStack
        self.subscriber = RedisSubscriber(
            PUBSUB_KEYS.EVENT_BAR_FILTER_VSA, None, self.Run)
        self.filter = FilterFirst()
        self.sdz = FilterKeyLevels()
        self.abcd = FilterAbcdPattern()
        self.pivot = FilterPivotPoint()
        self.cs = FilterCandlePattern()
        self.trend = FilterTrends()

    def Run(self, data):
        try:
            symbol = data['symbol']
            period = data['period']
            content = data['data']
            df = pd.DataFrame(content)
            df.rename(columns={'c': 'Close', 'o': 'Open', 'h': 'High', 'l': 'Low', 'v': 'Volume', 't': 'Date'}, inplace=True)
            if self.filter.IsFilter(symbol, df):
                return
            app1 = volumeSpreadAnalysis()
            vsa = app1.Run(symbol, df)
            close = df.iloc[0]['Close']
            if FilterPriceSpread.IsEnoughSpread(df, 0.3):
                fMinMax = TightMinMax(tightMinMaxN=2)
                isFirstMin, dfMinMax = fMinMax.Run(df)
                # 1 engulfing candle
                # 2 morning/evening star candle
                # candlestickparttern = self.cs.Run(symbol, df)
                candlestickparttern = 0
                # 4 for ABCD pattern
                if self.abcd.Run(symbol, df, dfMinMax=dfMinMax):
                    candlestickparttern += 4
                # 8 for Pivot Point pattern
                # if self.pivot.Run(symbol, df, close):
                #     candlestickparttern += 8
                if self.trend.Run(symbol, df, dfMinMax, isFirstMin):
                    candlestickparttern += 8

                # 16 for Key Level trading
                high = df.iloc[0]['High']
                low = df.iloc[0]['Low']
                if self.sdz.Run(symbol, df, dfMinMax=dfMinMax):
                    candlestickparttern += 16
                self.publisher.publish({
                    'datatype': 'VSA', 
                    'symbol': symbol, 
                    'timeframe': period, 
                    'vsa': vsa, 
                    'cs': candlestickparttern,
                    'price': close })
        except Exception as e:
            logging.warning(
                f'Error EventBarDataProcess.filterCheck - {data} {e}')

    def start(self):
        try:
            self.subscriber.start()
        except KeyboardInterrupt:
            self.subscriber.stop()
        except Exception as e:
            logging.warning(
                f'Error EventBarDataProcess.start - {e}')

    @staticmethod
    def run():
        logging.info(
            'EventBarDataProcess.run')
        app = EventBarDataProcess()
        app.start()


if __name__ == "__main__":
    pass

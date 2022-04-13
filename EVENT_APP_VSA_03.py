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

class EventBarDataProcess:

    def __init__(self, pubKeyStack=None, pubTrade=None):
        # StoreStack: class to access the redis Stack.
        self.publisher = RedisPublisher(
            PUBSUB_KEYS.EVENT_BAR_STACK_ADD) if pubKeyStack is None else pubKeyStack
        self.subscriber = RedisSubscriber(
            PUBSUB_KEYS.EVENT_BAR_FILTER_VSA, None, self.Run)
        self.filter = FilterFirst()
        self.sdz = FilterDailySupplyDemandZone()

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
            app2 = FilterCandlePattern()
            candlestickparttern = app2.Run(symbol, df)
            close = df.iloc[0]['Close']
            supplyDemandZone = self.sdz.Run(symbol, df, close)
            self.publisher.publish({
                'datatype': 'VSA', 
                'symbol': symbol, 
                'timeframe': period, 
                'vsa': vsa, 
                'cs': candlestickparttern,
                'sd': supplyDemandZone,
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

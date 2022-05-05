import logging
import datetime
import json

from redis import Redis
from redisTimeseriesData import RealTimeBars
from redisPubsub import RedisSubscriber, RedisPublisher
from pubsubKeys import PUBSUB_KEYS
from redisUtil import RedisTimeFrame

class EventBarHandleRealtimeData:
    '''A 1-Minute Bar happened.  Save the data.  And get 2 min and 5 min data for analysis later.'''

    def __init__(self, pubDataCheck=None, pubDataSave=None):
        self.rtb = RealTimeBars()
        self.publisher = RedisPublisher(
            PUBSUB_KEYS.EVENT_BAR_FILTER_VSA) if pubDataCheck is None else pubDataCheck
        self.subscriber = RedisSubscriber(
            PUBSUB_KEYS.EVENT_BAR_CANDIDATE, None, self.AddBar)

    def makePubData(self, symbol: str, timeframe: str, data: list):
        return {
            "symbol": symbol,
            "period": timeframe,
            "data": data
        }

    def isTimeInterval(self, timeframe:str) -> bool:
        timeIntervals = {
            # RedisTimeFrame.MIN2: 2,
            RedisTimeFrame.MIN5: 5,
            RedisTimeFrame.MIN15: 15
        }
        min = timeIntervals.get(timeframe, -1)
        if min <= 0:
            return False
        moment = datetime.datetime.now()
        # kyd time-interval
        if moment.minute % min == 0:
            return True
        return False

    def publish2Min(self, symbol: str, timeframe: str):
        data2 = self.rtb.RedisGetRealtimeData(None, symbol, timeframe)
        if isinstance(data2, dict):
            arrLen = len(data2['data']) if 'data' in data2.keys() else 0
            if data2 is not None and arrLen >= 3:
                self.publisher.publish(data2)
            else:
                logging.info(
                    f"EventBarHandleRealtimeData.publish2Min: Not Enough {symbol} {timeframe} {arrLen}")

    def AddBar(self, data=None):
        try:
            symbol: str = ''
            if data is None:
                symbol = 'FANG'
            else:
                symbol = data['S']
                self.rtb.RedisAddBar(data)
                self.rtb.RedisAddBarAggregation(data)
            if self.isTimeInterval(RedisTimeFrame.MIN2):
                self.publish2Min(symbol, RedisTimeFrame.MIN2)
            if self.isTimeInterval(RedisTimeFrame.MIN5):
                self.publish2Min(symbol, RedisTimeFrame.MIN5)
            if self.isTimeInterval(RedisTimeFrame.MIN15):
                self.publish2Min(symbol, RedisTimeFrame.MIN15)
        except Exception as e:
            logging.error(
                f"Error EVENT_BAR_CANDIDATE.EventBarHandleRealtimeData.AddBar {e} {data} ")

    def start(self):
        try:
            self.subscriber.start()
        except KeyboardInterrupt:
            self.subscriber.stop()
        except Exception as e:
            logging.error(e)

    @staticmethod
    def run():
        logging.info("EVENT_BAR_HANDLE_REALTIME_DATA.EventBarHandleRealtimeData.run")
        eventBarCandidate = EventBarHandleRealtimeData()
        eventBarCandidate.start()


if __name__ == "__main__":
    logging.info("EVENT_BAR_HANDLE_REALTIME_DATA.EventBarHandleRealtimeData.run")
    ebc = EventBarHandleRealtimeData()
    #data2 = ebc.rtb.RedisGetRealtimeData(None, 'MSFT', RedisTimeFrame.MIN2)
    ebc.AddBar()
    # ebc.run()


# input:    { 'c': 136.02, 'h': 136.06, 'l': 136.0, 'o': 136.04, 'S': 'ALLE', 't': 1627493640000000000, 'v': 712})
# output:
# {
#     "symbol": "ALLE",
#     "period": "1MIN",
#     "data": [
#         {
#             "timestamp": 000010,
#             "close": 136.02,
#             "high": 136.06,
#             "low": 136.0,
#             "open": 136.04,
#             "volume": 712
#         },
#         {
#             "timestamp": 000009,
#             "close": 136.02,
#             "high": 136.06,
#             "low": 136.0,
#             "open": 136.04,
#             "volume": 712
#         },
#         {
#             "timestamp": 000008,
#             "close": 136.02,
#             "high": 136.06,
#             "low": 136.0,
#             "open": 136.04,
#             "volume": 712
#         },
#         {
#             "timestamp": 000007,
#             "close": 136.02,
#             "high": 136.06,
#             "low": 136.0,
#             "open": 136.04,
#             "volume": 712
#         },
#         {
#             "timestamp": 000006,
#             "close": 136.02,
#             "high": 136.06,
#             "low": 136.0,
#             "open": 136.04,
#             "volume": 712
#         }
#     ]
# }

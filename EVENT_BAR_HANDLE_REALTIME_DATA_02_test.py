from unittest import mock, TestCase
from testUtil import TestPublisher
from EVENT_BAR_HANDLE_REALTIME_DATA_02 import EventBarHandleRealtimeData
from RedisTimeseriesTable import TimeseriesTable
from redisUtil import TimeStamp, RedisTimeFrame
from redisTimeseriesData import RealTimeBars


class TestEventBarCandidateCheck(TestCase):

    def setUp(self) -> None:
        self.symbol = 'TEST'
        app = TimeseriesTable()
        app.RemoveStock(self.symbol)
        app.CreateRedisStockSymbol([self.symbol])
        self.timestamp = TimeStamp.now() - 600
        self.data = {'o': 11.1, 'c': 11.0, 'h': 11.3, 'l': 10.05,
                     'v': 2700000, 'S': self.symbol, 't': self.timestamp}
        self.rtb = RealTimeBars()
        self.hitCount = 0

    def tearDown(self) -> None:
        app = TimeseriesTable()
        app.RemoveStock(self.symbol)

    def tearDown(self):
        self.data = None

    def doNothing(self, data):
        self.hitCount += 1

    def test_event_bar_candidate_pass_2(self):
        pubPush = TestPublisher(self.doNothing)
        pubSave = TestPublisher(self.doNothing)
        for i in range(5):
            process1 = EventBarHandleRealtimeData(pubPush, pubSave)
            self.timestamp += 60
            self.data['t'] = self.timestamp
            process1.AddBar(self.data)
        data = self.rtb.RedisGetRealtimeData(
            None, self.symbol, RedisTimeFrame.MIN1)
        self.assertEqual(len(data['data']), 5)

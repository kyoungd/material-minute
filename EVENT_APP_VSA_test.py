from unittest import mock, TestCase
from testUtil import TestPublisher
from EVENT_BAR_HANDLE_REALTIME_DATA_02 import EventBarHandleRealtimeData
from RedisTimeseriesTable import TimeseriesTable
from redisUtil import TimeStamp, RedisTimeFrame
from redisTimeseriesData import RealTimeBars
import pandas as pd
from EVENT_APP_VSA_03 import EventBarDataProcess
from filterFirst import FilterFirst

class TestEventAppVolumeSpreadAnalysis(TestCase):

    def setUp(self) -> None:
        self.app = EventBarDataProcess()

    def dataSetup(self, price, isFirstMin, p0, p1, p2, p3, p4, p5, v0, v1, v2, v3, v4, v5):
        data = {'Date':
                ['2021-01-07T00:00:00.000000000', '2021-02-01T00:00:00.000000000',
                 '2021-03-12T00:00:00.000000000', '2021-04-23T00:00:00.000000000',
                 '2021-05-28T00:00:00.000000000', '2021-09-01T00:00:00.000000000'],
                'Close':
                    [p0+0.1, p1+0.1, p2+0.1,
                     p3+0.1, p4+0.1, p5+0.1],
                'Volume':
                    [v0+0.1, v1+0.1, v2+0.1,
                     v3+0.1, v4+0.1, v5+0.1],
                'High':
                    [p0+1.01, p1+1.01, p2+1.01,
                     p3+1.01, p4+1.01, p5+1.01],
                'Low':
                    [p0-1.01, p1-1.01, p2-1.01,
                     p3-1.01, p4-1.01, p5-1.01],
                'Open':
                    [p0-0.5, p1-0.5, p2-0.5,
                     p3-0.5, p4-0.5, p5-0.5]
                }
        df = pd.DataFrame(data)
        return df

    def test_event_bar_candidate_pass(self):
        symbol = 'AAPL'
        period = RedisTimeFrame.MIN15
        data = {'symbol': symbol, 'period': period}
        data = self.app.Run(data)
        self.assertEqual(data, None)

    def test_PriceFilter(self):
        df:pd.DataFrame = self.dataSetup(100.1, False, 4, 10, 15, 20, 25, 30, 200000, 200000, 200000, 200000, 200000, 200000)
        app = FilterFirst()
        result = app.IsFilter("TEST", df)
        self.assertEqual(result, True)

    def test_VolumeFilter(self):
        df:pd.DataFrame = self.dataSetup(100.1, False, 4, 10, 15, 20, 25, 30, 2000, 200000, 200000, 200000, 200000, 200000)
        app = FilterFirst()
        result = app.IsFilter("TEST", df)
        self.assertEqual(result, True)

    def test_AtrFilter(self):
        df:pd.DataFrame = self.dataSetup(100.1, False, 200, 199, 199, 200, 199, 199, 200000, 200000, 200000, 200000, 200000, 200000)
        app = FilterFirst()
        result = app.IsFilter("TEST", df)
        self.assertEqual(result, True)

    def test_AtrFilter_Pass(self):
        df: pd.DataFrame = self.dataSetup(
            100.1, False, 200, 189, 189, 200, 179, 199, 200000, 200000, 200000, 200000, 200000, 200000)
        app = FilterFirst()
        result = app.IsFilter("TEST", df)
        self.assertEqual(result, False)

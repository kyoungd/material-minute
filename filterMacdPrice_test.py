import unittest
import pandas as pd
from filterMacdPrice import FilterMacdPrice
from testUtil import TestUtil
from utilAlpacaHistoricalBarData import AlpacaHistoricalBarData
from alpacaHistorical import TimePeriod
from util import TestUtil


class TestFilterMacdPrice(unittest.TestCase):
    def setUp(self):
        pass

    def executeApp(self, symbol, endDate, endHour, endMinute, timeframe):
        isOk, df = TestUtil.getRealtimeData(
            symbol, endDate, endHour, endMinute, timeframe)
        pp = FilterMacdPrice()
        result = pp.Run(symbol, df, timeframe)
        return result

    # 2022/04/29 4:30 AM - 7:45 PM PST
    def testMacdPrice_01(self):
        result = self.executeApp(
            'UONE', '2022-06-06', 9, 14, TimePeriod.Min2.value)
        self.assertTrue(result)

    # 2022/04/29 4:30 AM - 7:45 PM PST
    def testMacdPrice_02(self):
        result = self.executeApp(
            'UONE', '2022-06-06', 9, 45, TimePeriod.Min5.value)
        self.assertTrue(result)

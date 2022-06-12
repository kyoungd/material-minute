import unittest
import pandas as pd
from testUtil import TestUtil
from filterTrend import FilterTrends
from alpacaHistorical import TimePeriod
from tightMinMax import TightMinMax


class TestFilterTrendRealData(unittest.TestCase):
    def executeApp(self, symbol, endDate, endHour, endMinute, timeframe):
        isOk, df = TestUtil.getRealtimeData(
            symbol, endDate, endHour, endMinute, timeframe)
        fMinmax = TightMinMax(tightMinMaxN=2)
        isFirstMin, dfMinMax = fMinmax.Run(df)
        app = FilterTrends()
        result = app.Run(symbol, df, dfMinMax, isFirstMin)
        return result

    def testTrendsReal_01(self):
        result = self.executeApp("CNCE", '2022-05-27', 6, 40, TimePeriod.Min2.value)
        self.assertTrue(result)

    def testTrendsReal_02(self):
        result = self.executeApp("SIGA", '2022-05-27',
                                 7, 25, TimePeriod.Min5.value)
        self.assertTrue(result)

    def testTrendsReal_03(self):
        result = self.executeApp("SIGA", '2022-05-27',
                                 7, 15, TimePeriod.Min15.value)
        self.assertTrue(result)

import unittest
import pandas as pd
from util import TestUtil
from filterKeylevels import FilterKeyLevels
from alpacaHistorical import TimePeriod


class TestFilterKeyLevelsRealData(unittest.TestCase):

    def executeApp(self, symbol, endDate, endHour, endMinute, timeframe, keylevels):
        isOk, df = TestUtil.getRealtimeData(
            symbol, endDate, endHour, endMinute, timeframe)
        sd = FilterKeyLevels()
        return sd.Run(symbol, df, keylevels)

    def testKeyLevelsReal_01(self):
        keylevels = [
            {"Date":"2022-05-18T04:00:00Z","Close":243.25,"Type":"max"},
            {"Date":"2022-05-16T04:00:00Z","Close":191.66,"Type":"min"},
            {"Date":"2022-05-13T04:00:00Z","Close":200.09,"Type":"max"}
        ]
        result = self.executeApp('VRTX', '2022-05-13',
                                 8, 30, TimePeriod.Min15.value, keylevels)
        self.assertTrue(result)


    def testKeyLevelsReal_02(self):
        keylevels = [
            {"Date":"2022-05-18T04:00:00Z","Close":67.45,"Type":"max"},
            {"Date":"2022-05-16T04:00:00Z","Close":53.15,"Type":"min"},
            {"Date":"2022-05-13T04:00:00Z","Close":71.09,"Type":"max"}
        ]
        result = self.executeApp('BJ', '2022-05-18',
                                 8, 30, TimePeriod.Min15.value, keylevels)
        self.assertTrue(result)

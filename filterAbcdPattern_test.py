import unittest
import pandas as pd
from filterAbcdPattern import FilterAbcdPattern
from alpacaHistorical import TimePeriod
from testUtil import TestUtil


class TestFilterAbcdRealData(unittest.TestCase):

    def executeApp(self, symbol:str, endDate:str, endHour:int, endMinute:int, timeframe:str):
        isOk, df = TestUtil.getRealtimeData(
            symbol, endDate, endHour, endMinute, timeframe)
        abcd = FilterAbcdPattern()
        return abcd.Run(symbol, df, None)

    def testAbcdRealData_01(self):
        result = self.executeApp('WBD', '2022-04-29',
                                 9, 15, TimePeriod.Min15.value)
        self.assertFalse(result)

    def testAbcdRealData_02(self):
        result = self.executeApp('RIOT', '2022-04-28',
                                 9, 15, TimePeriod.Min15.value)
        self.assertFalse(result)

    # 2022/04/28 7:30 AM - 12:00 AM EST
    def testAbcdRealData_03(self):
        result = self.executeApp('CRBU', '2022-05-13',
                                 7, 5, TimePeriod.Min5.value)
        self.assertTrue(result)

    def testAbcdRealData_04(self):
        result = self.executeApp('PTON', '2022-05-13',
                                 8, 0, TimePeriod.Min15.value)
        self.assertTrue(result)

    def testAbcdRealData_05(self):
        result = self.executeApp('BWV', '2022-05-03',
                                 12, 0, TimePeriod.Min15.value)
        self.assertFalse(result)

    def testAbcdRealData_06(self):
        result = self.executeApp('PTON', '2022-05-03',
                                 8, 15, TimePeriod.Min15.value)
        self.assertFalse(result)

    def testAbcdRealData_07(self):
        result = self.executeApp('AFRM', '2022-05-17',
                                 8, 0, TimePeriod.Min5.value)
        self.assertTrue(result)
        
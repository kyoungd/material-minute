import unittest
import pandas as pd
from filterAbcdPattern import FilterAbcdPattern
from testUtil import TestUtil
from alpacaHistorical import TimePeriod
from util import TestUtil


class TestFilterAbcdPattern(unittest.TestCase):

    def testAbcdPattern_01(self):
        seed = [26.5, 26, 25, 24, 23, 25, 26, 27, 25, 24, 23, 22, 23, 24, 
                23, 24, 23, 24, 23, 24, 23, 24, 23, 24, 23, 24, 23, 24,
                23, 24, 23, 24, 23, 24, 23, 24, 23, 24, 23, 24, 23, 24,
                23, 24, 23, 24, 23, 24, 23, 24, 23, 24, 23, 24, 23, 24]
        df = TestUtil.dfSetup(seed)
        app = FilterAbcdPattern()
        result = app.Run('AAPL', df, 26.8)
        self.assertEqual(result, True)

    def testAbcdPattern_02(self):
        seed = [23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34,
                23, 24, 23, 24, 23, 24, 23, 24, 23, 24, 23, 24, 23, 24,
                23, 24, 23, 24, 23, 24, 23, 24, 23, 24, 23, 24, 23, 24,
                23, 24, 23, 24, 23, 24, 23, 24, 23, 24, 23, 24, 23, 24]
        df = TestUtil.dfSetup(seed)
        app = FilterAbcdPattern()
        result = app.Run('AAPL', df, 23.5)
        self.assertEqual(result, False)

    def testAbcdPattern_03(self):
        seed = [23, 22, 21, 20, 21, 22, 23, 24, 25, 24, 23, 22, 23, 24,
                23, 24, 23, 24, 23, 24, 23, 24, 23, 24, 23, 24, 23, 24,
                23, 24, 23, 24, 23, 24, 23, 24, 23, 24, 23, 24, 23, 24,
                23, 24, 23, 24, 23, 24, 23, 24, 23, 24, 23, 24, 23, 24]
        df = TestUtil.dfSetup(seed)
        app = FilterAbcdPattern()
        result = app.Run('AAPL', df, 20.5)
        self.assertEqual(result, False)

    def testAbcdPattern_04(self):
        seed = [26.5, 26, 25, 24, 23, 25, 26, 27, 25, 24, 23, 22, 23, 24,
                23, 24, 23, 24, 23, 24, 23, 24, 23, 24, 23, 24, 23, 24,
                23, 24, 23, 24, 23, 24, 23, 24, 23, 24, 23, 24, 23, 24,
                23, 24, 23, 24, 23, 24, 23, 24, 23, 24, 23, 24, 23, 24]
        df = TestUtil.dfSetup(seed[::-1])
        app = FilterAbcdPattern()
        result = app.Run('AAPL', df, 24.2)
        self.assertEqual(result, False)

    def testAbcdPattern_05(self):
        seed = [19, 21, 22, 23, 24, 23, 22, 21, 20, 19, 20, 21, 22, 23, 24, 25, 26, 25, 24,
                23, 24, 23, 24, 23, 24, 23, 24, 23, 24, 23, 24, 23, 24,
                23, 24, 23, 24, 23, 24, 23, 24, 23, 24, 23, 24, 23, 24,
                23, 24, 23, 24, 23, 24, 23, 24, 23, 24, 23, 24, 23, 24]
        df = TestUtil.dfSetup(seed)
        app = FilterAbcdPattern()
        result = app.Run('AAPL', df, 19)
        self.assertEqual(result, True)


class TestFilterAbcdRealData(unittest.TestCase):

    def executeApp(self, symbol:str, endDate:str, endHour:int, endMinute:int, timeframe:str):
        isOk, df = TestUtil.getRealtimeData(
            symbol, endDate, endHour, endMinute, timeframe)
        abcd = FilterAbcdPattern()
        return abcd.Run(symbol, df, 0)

    # 2022/04/29 7:30 AM - 12:15 AM EST
    def testAbcdRealData_01(self):
        result = self.executeApp('WBD', '2022-04-29',
                                 11, 15, TimePeriod.Min15.value)
        self.assertTrue(result)
        

    def testAbcdRealData_02(self):
        result = self.executeApp('RIOT', '2022-04-28',
                                 11, 30, TimePeriod.Min15.value)
        self.assertTrue(result)

        

    # 2022/04/28 7:30 AM - 12:00 AM EST
    def testAbcdRealData_03(self):
        result = self.executeApp('TQQQ', '2022-04-28',
                                 9, 00, TimePeriod.Min15.value)
        self.assertTrue(result)


    def testAbcdRealData_04(self):
        result = self.executeApp('BWV', '2022-05-03',
                                 12, 0, TimePeriod.Min5.value)
        self.assertTrue(result)

    def testAbcdRealData_05(self):
        result = self.executeApp('BWV', '2022-05-03',
                                 12, 0, TimePeriod.Min15.value)
        self.assertFalse(result)

    def testAbcdRealData_06(self):
        result = self.executeApp('CHGG', '2022-05-04',
                                 12, 25, TimePeriod.Min5.value)
        self.assertTrue(result)

    def testAbcdRealData_07(self):
        result = self.executeApp('CHGG', '2022-05-04',
                                 8, 15, TimePeriod.Min5.value)
        self.assertTrue(result)

    def testAbcdRealData_08(self):
        result = self.executeApp('CHGG', '2022-05-04',
                                 12, 0, TimePeriod.Min15.value)
        self.assertTrue(result)

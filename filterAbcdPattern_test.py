from datetime import datetime, timedelta
import unittest
import pandas as pd
from filterAbcdPattern import FilterAbcdPattern
from testUtil import TestUtil
from utilAlpacaHistoricalBarData import AlpacaHistoricalBarData
from alpacaHistorical import TimePeriod

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

    # 2022/04/29 7:30 AM - 12:15 AM EST
    def testAbcdRealData_01(self):
        app = AlpacaHistoricalBarData(
            'WBD', '2022-04-29T11:30:00Z',
            '2022-04-29T16:15:00Z', TimePeriod.Min15.value)
        isOk, df = app.GetDataFrame()
        abcd = FilterAbcdPattern()
        result = abcd.Run('WBD', df, 0)
        # print(df)
        self.assertTrue(result)
        

    def testAbcdRealData_02(self):
        app = AlpacaHistoricalBarData(
            'RIOT', '2022-04-28T11:30:00Z',
            '2022-04-28T16:30:00Z', TimePeriod.Min15.value)
        isOk, df = app.GetDataFrame()
        abcd = FilterAbcdPattern()
        result = abcd.Run('RIOT', df, 0)
        self.assertTrue(result)

        

    # 2022/04/28 7:30 AM - 12:00 AM EST
    def testAbcdRealData_03(self):
        app = AlpacaHistoricalBarData(
            'TQQQ', '2022-04-28T11:30:00Z',
            '2022-04-28T16:00:00Z', TimePeriod.Min15.value)
        isOk, df = app.GetDataFrame()
        abcd = FilterAbcdPattern()
        result = abcd.Run('TQQQ', df, 0)
        self.assertTrue(result)


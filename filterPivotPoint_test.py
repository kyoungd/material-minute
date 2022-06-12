from datetime import datetime, timedelta
import unittest
import pandas as pd
from filterPivotPoint import FilterPivotPoint
from utilAlpacaHistoricalBarData import AlpacaHistoricalBarData
from alpacaHistorical import TimePeriod
from testUtil import TestUtil

class TestFilterPivotPoint(unittest.TestCase):
    def setUp(self):
        pass

    def executeApp(self, symbol, endDate, endHour, endMinute, timeframe, pivotValue):
        isOk, df = TestUtil.getRealtimeData(symbol, endDate, endHour, endMinute, timeframe)
        pivot = {
            "pp": pivotValue,
            "s1": pivotValue * 1.05,
            "r1": pivotValue * 0.95
        }
        pp = FilterPivotPoint()
        result = pp.IsPivotPointCenter(pivot, df, 0)
        return result

    # 2022/04/29 4:30 AM - 7:45 PM PST
    def testCenterPivotReal_01(self):
        result = self.executeApp('WBD', '2022-04-29', 7, 45, TimePeriod.Min15.value, 18.56)
        self.assertTrue(result)


    # 2022/04/28 4:30 AM - 11:30 PM PST
    def testCenterPivotReal_02(self):
        pivot = {
            "pp": 11.24,
            "s1": 12.46,
            "r1": 10.01
        }
        symbol = 'RIOT'
        onedate = '2022-04-28'
        startt = '11:30:00'
        endt = '18:45:00'
        starttime = f'{onedate}T{startt}Z'
        endtime = f'{onedate}T{endt}Z'
        timeframe = TimePeriod.Min15.value
        app = AlpacaHistoricalBarData(symbol, starttime, endtime, timeframe)
        isOk, df = app.GetDataFrame()
        pp = FilterPivotPoint()
        result = pp.IsPivotPointCenter(pivot, df, 0)
        self.assertTrue(result)


    # 2022/05/02 4:30 AM - 11:35 AM PST
    def testCenterPivotReal_03(self):
        pivot = {
            "pp": 6.92,
            "s1": 7.92,
            "r1": 5.92
        }
        symbol = 'RDBX'
        onedate = '2022-05-04'
        startt = '11:30:00'
        endt = '16:35:00'
        timeframe = TimePeriod.Min5.value
        starttime = f'{onedate}T{startt}Z'
        endtime = f'{onedate}T{endt}Z'
        app = AlpacaHistoricalBarData(symbol, starttime, endtime, timeframe)
        isOk, df = app.GetDataFrame()
        pp = FilterPivotPoint()
        result = pp.IsPivotPointCenter(pivot, df, 0)
        self.assertTrue(result)


    # 2022/05/02 4:30 AM - 6:50 AM PST
    def testCenterPivotReal_04(self):
        pivot = {
            "pp": 12.16,
            "s1": 13.16,
            "r1": 11.16
        }
        symbol = 'KZR'
        onedate = '2022-05-02'
        startt = '11:30:00'
        endt = '13:50:00'
        timeframe = TimePeriod.Min5.value
        starttime = f'{onedate}T{startt}Z'
        endtime = f'{onedate}T{endt}Z'
        app = AlpacaHistoricalBarData(symbol, starttime, endtime, timeframe)
        isOk, df = app.GetDataFrame()
        pp = FilterPivotPoint()
        result = pp.IsPivotPointCenter(pivot, df, 0)
        self.assertTrue(result)


    # 2022/05/02 4:30 AM - 6:50 AM PST
    def testCenterPivotReal_05(self):
        result = self.executeApp('KZR', '2022-05-02', 6, 50, TimePeriod.Min5.value, 12.16)
        self.assertTrue(result)

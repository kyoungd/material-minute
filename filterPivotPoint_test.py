from datetime import datetime, timedelta
import unittest
import pandas as pd
from filterPivotPoint import FilterPivotPoint
from testUtil import TestUtil
from utilAlpacaHistoricalBarData import AlpacaHistoricalBarData
from alpacaHistorical import TimePeriod


class TestFilterPivotPoint(unittest.TestCase):
    def setUp(self):
        pass

    # 2022/04/29 4:30 AM - 7:45 PM PST
    def testCenterPivotReal_01(self):
        pivot = {
            "pp": 18.56,
            "s1": 20.02,
            "r1": 17.01
        }
        symbol = 'WBD'
        starttime = '2022-04-29T11:30:00Z'
        endtime = '2022-04-29T14:45:00Z'
        timeframe = TimePeriod.Min15.value
        app = AlpacaHistoricalBarData(symbol, starttime, endtime, timeframe)
        isOk, df = app.GetDataFrame()
        pp = FilterPivotPoint()
        result = pp.IsPivotPointCenter(pivot, df, 0)
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


    # 2022/04/29 4:30 AM - 
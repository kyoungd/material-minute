from datetime import datetime, timedelta
import unittest
import pandas as pd
from testUtil import TestUtil
from filterSupplyDemandZone import FilterDailySupplyDemandZone
from utilAlpacaHistoricalBarData import AlpacaHistoricalBarData
from alpacaHistorical import TimePeriod

class TestFilterSupplyDemandZone(unittest.TestCase):

    def setUp(self) -> None:
        self.app = FilterDailySupplyDemandZone()

    def testSupplyDemand_01(self):
        seed = [113, 114, 115,
                114, 113, 112, 111, 105, 103, 99, 95, 90, 88, 85,
                88, 90, 92, 95, 99, 104, 110, 116, 124, 130, 135,
                134, 131, 129, 124, 120, 119,
                120, 123, 127, 129,
                130, 125, 120, 125, 120, 119, 118, 117, 110]
        df = TestUtil.dfSetup(seed)
        result1 = self.app.Run('abc', df, 0)
        self.assertEqual(result1, True)

    def testSupplyDemand_02(self):
        seed = [85.4, 90, 95, 100, 105, 110, 113, 114, 115,
                114, 113, 112, 111, 105, 103, 99, 95, 90, 88, 85,
                88, 90, 92, 95, 99, 104, 110, 116, 124, 130, 135,
                134, 131, 129, 124, 120, 119,
                120, 123, 127, 129,
                130, 125, 120, 125, 120, 119, 118, 117, 110]
        df = TestUtil.dfSetup(seed)
        result1 = self.app.Run('abc', df, 0)
        self.assertEqual(result1, True)

    def testSupplyDemand_03(self):
        seed = [125, 120, 115, 110, 113, 114, 115,
                114, 113, 112, 111, 105, 103, 99, 95, 90, 88, 85,
                88, 90, 92, 95, 99, 104, 110, 116, 124, 130, 135,
                134, 131, 129, 124, 120, 119,
                120, 123, 127, 129,
                130, 125, 120, 125, 120, 119, 118, 117, 110]
        df = TestUtil.dfSetup(seed)
        result1 = self.app.Run('abc', df, 0)
        self.assertEqual(result1, False)


class TestFilterSupplyDemandRealData(unittest.TestCase):
    
    # 2022/04/29 7:30 AM - 12:45 PM EST
    def testSupplyDemandReal_01(self):
        app = AlpacaHistoricalBarData(
            'TQQQ', '2022-04-27T11:30:00Z',
            '2022-04-27T16:45:00Z', TimePeriod.Min15.value)
        isOk, df = app.GetDataFrame()
        sd = FilterDailySupplyDemandZone()
        result = sd.Run('TQQQ', df, 0)
        self.assertTrue(result)


    # 2022/04/28 7:30 AM - 3:00 PM EST
    def testSupplyDemandReal_02(self):
        app = AlpacaHistoricalBarData(
            'RIOT', '2022-04-28T11:30:00Z',
            '2022-04-28T18:45:00Z', TimePeriod.Min15.value)
        isOk, df = app.GetDataFrame()
        sd = FilterDailySupplyDemandZone()
        result = sd.Run('RIOT', df, 0)
        self.assertTrue(result)


    # 2022/04/28 7:30 AM - 3:00 PM EST
    def testSupplyDemandReal_03(self):
        app = AlpacaHistoricalBarData(
            'RIOT', '2022-04-28T11:30:00Z',
            '2022-04-28T18:45:00Z', TimePeriod.Min15.value)
        isOk, df = app.GetDataFrame()
        sd = FilterDailySupplyDemandZone()
        result = sd.Run('RIOT', df, 0)
        self.assertTrue(result)


    # 2022/04/28 7:30 AM - 3:00 PM EST
    def testSupplyDemandReal_03(self):
        app = AlpacaHistoricalBarData(
            'RIOT', '2022-04-28T11:30:00Z',
            '2022-04-28T18:45:00Z', TimePeriod.Min15.value)
        isOk, df = app.GetDataFrame()
        sd = FilterDailySupplyDemandZone()
        result = sd.Run('RIOT', df, 0)
        self.assertTrue(result)


    # 2022/04/28 4:30 AM - 10:30 AM PST
    def testSupplyDemandReal_04(self):
        app = AlpacaHistoricalBarData(
            'RIOT', '2022-04-28T11:30:00Z',
            '2022-04-28T17:30:00Z', TimePeriod.Min15.value)
        isOk, df = app.GetDataFrame()
        sd = FilterDailySupplyDemandZone()
        result = sd.Run('RIOT', df, 0)
        self.assertFalse(result)



    # 2022/04/28 4:30 AM - 9:45 AM PST
    def testSupplyDemandReal_05(self):
        symbol = 'WBD'
        starttime = '2022-04-28T11:30:00Z'
        endtime = '2022-04-28T16:45:00Z'
        timeframe = TimePeriod.Min15.value
        app = AlpacaHistoricalBarData(symbol, starttime, endtime, timeframe)
        isOk, df = app.GetDataFrame()
        sd = FilterDailySupplyDemandZone()
        result = sd.Run('RIOT', df, 0)
        self.assertTrue(result)


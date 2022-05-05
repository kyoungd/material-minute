import unittest
import pandas as pd
from util import TestUtil
from filterSupplyDemandZone import FilterDailySupplyDemandZone
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

    def executeApp(self, symbol, endDate, endHour, endMinute, timeframe):
        isOk, df = TestUtil.getRealtimeData(
            symbol, endDate, endHour, endMinute, timeframe)
        sd = FilterDailySupplyDemandZone()
        return sd.Run(symbol, df, 0)

    def testSupplyDemandReal_01(self):
        result = self.executeApp('TQQQ', '2022-04-27', 9, 45, TimePeriod.Min15.value)
        self.assertTrue(result)


    # 2022/04/28 7:30 AM - 3:00 PM EST
    def testSupplyDemandReal_02(self):
        result = self.executeApp('RIOT', '2022-04-28',
                                 11, 45, TimePeriod.Min15.value)
        self.assertTrue(result)


    # 2022/04/28 4:30 AM - 10:30 AM PST
    def testSupplyDemandReal_04(self):
        result = self.executeApp('RIOT', '2022-04-28',
                                 10, 30, TimePeriod.Min15.value)
        self.assertFalse(result)


    # 2022/04/28 4:30 AM - 9:45 AM PST
    def testSupplyDemandReal_05(self):
        result = self.executeApp('WBD', '2022-04-28',
                                 11, 45, TimePeriod.Min15.value)
        self.assertTrue(result)


    def testSupplyDemandReal_06(self):
        result = self.executeApp('RDBX', '2022-05-04', 12, 30, TimePeriod.Min15.value)
        self.assertTrue(result)


    def testSupplyDemandReal_07(self):
        result = self.executeApp('RVLV', '2022-05-02', 10, 45, TimePeriod.Min15.value)
        self.assertTrue(result)

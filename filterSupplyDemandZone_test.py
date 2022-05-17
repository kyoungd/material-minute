import unittest
import pandas as pd
from util import TestUtil
from filterSupplyDemandZone import FilterDailySupplyDemandZone
from alpacaHistorical import TimePeriod

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
                                 10, 40, TimePeriod.Min15.value)
        self.assertTrue(result)


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

    def testSupplyDemandReal_08(self):
        result = self.executeApp('VERU', '2022-05-13', 11, 35, TimePeriod.Min15.value)
        self.assertFalse(result)

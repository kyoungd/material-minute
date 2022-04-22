from datetime import datetime, timedelta
import unittest
import pandas as pd
from testUtil import TestUtil
from filterSupplyDemandZone import FilterDailySupplyDemandZone

class TestFilterSupplyDemandZone(unittest.TestCase):

    def setUp(self) -> None:
        seed = [113, 114, 115,
                114, 113, 112, 111, 105, 103, 99, 95, 90, 88, 85,
                88, 90, 92, 95, 99, 104, 110, 116, 124, 130, 135,
                134, 131, 129, 124, 120, 119,
                120, 123, 127, 129,
                130, 125, 120, 125, 120, 119, 118, 117, 110]
        self.df = TestUtil.dfSetup(seed)
        self.app = FilterDailySupplyDemandZone()

    def testSupplyDemand_01(self):
        result1 = self.app.Run('abc', self.df, 115.4)
        self.assertEqual(result1, False)

    def testSupplyDemand_02(self):
        result1 = self.app.Run('abc', self.df, 85.4)
        self.assertEqual(result1, True)

    def testSupplyDemand_03(self):
        result1 = self.app.Run('abc', self.df, 134.4)
        self.assertEqual(result1, True)

    def testSupplyDemand_04(self):
        result1 = self.app.Run('abc', self.df, 125.4)
        self.assertEqual(result1, False)

    def testSupplyDemand_05(self):
        result1 = self.app.Run('abc', self.df, 119.4)
        self.assertEqual(result1, False)

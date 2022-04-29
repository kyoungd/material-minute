from datetime import datetime, timedelta
import unittest
import pandas as pd
from filterPivotPoint import FilterPivotPoint, FilterCenterPivot
from testUtil import TestUtil


class TestFilterPivotPoint(unittest.TestCase):
    def setUp(self):
        pass

    def testPivotPoint_01(self):
        seed = [158, 159, 160, 163, 164, 161, 152, 143, 133, 123]
        df1 = TestUtil.dfSetup(seed)
        pivot = {
            "pp": 121.4,
            "s1": 186.8,
            "r1": 106.1
        }
        close = 156.8
        app = FilterPivotPoint()
        result = False
        if self.IsItReady(pivot, df1, close):
            result = app.IsPivotPointInPlay(pivot, df1, close)
        self.assertEqual(result, True)


    def testCenterPivot_02(self):
        seed = [22, 21, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 31, 30, 29]
        pivot = {
            "pp": 19.8,
            "s1": 27.2,
            "r1": 18.5
        }
        close = 20.1
        df = TestUtil.dfSetup(seed)
        app = FilterCenterPivot()
        result = app.IsInPlay(pivot, df, close)
        self.assertEqual(result, True)


    def testCenterPivot_03(self):
        seed = [22, 21, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
        pivot = {
            "pp": 19.8,
            "s1": 27.2,
            "r1": 18.5
        }
        close = 20.1
        df = TestUtil.dfSetup(seed)
        app = FilterCenterPivot()
        result = app.IsInPlay(pivot, df, close)
        self.assertEqual(result, True)

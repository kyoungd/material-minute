from datetime import datetime, timedelta
import unittest
import pandas as pd
from filterPivotPoint import FilterPivotPoint
from testUtil import TestUtil


class TestFilterPivotPoint(unittest.TestCase):
    def setUp(self):
        seed = [158, 159, 160, 163, 164, 161, 152, 143, 133, 123]
        self.df = TestUtil.dfSetup(seed)
        self.app = FilterPivotPoint()

    def testAbcdPattern_01(self):
        pivot = {
            "pp": 121.4,
            "s1": 186.8,
            "r1": 106.1
        }
        close = 156.8
        result = False
        if self.app.IsItReady(pivot, self.df, close):
            result = self.app.IsPivotPointInPlay(pivot, self.df, close)
        self.assertEqual(result, True)

from datetime import datetime, timedelta
import unittest
import pandas as pd
from filterPriceSpread import FilterPriceSpread
from testUtil import TestUtil


class TestFilterPriceSpread(unittest.TestCase):

    def testFilterPriceSpread_01(self):
        seed = [23, 22, 21, 20, 21, 22, 23, 24, 25, 24, 23, 22, 23, 24]
        df = TestUtil.dfSetup(seed)
        app = FilterPriceSpread()
        result = app.IsEnoughSpread(df, 0.05)
        self.assertEqual(result, True)


    def testFilterPriceSpread_02(self):
        seed = [23, 22, 22.5, 23, 22.7, 22.8, 23, 22.9, 22.8]
        df = TestUtil.dfSetup(seed)
        app = FilterPriceSpread()
        result = app.IsEnoughSpread(df, 0.15)
        self.assertEqual(result, False)


    def testFilterPriceSpread_slope(self):
        app = FilterPriceSpread()
        data1 = app.slope(100, 100, 200, 200, 150)
        self.assertEqual(data1, 150)
        data2 = app.slope(100, 100, 200, 300, 150)
        self.assertEqual(data2, 200)
    
        
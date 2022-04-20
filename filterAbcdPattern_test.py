from datetime import datetime, timedelta
import unittest
import pandas as pd
from filterAbcdPattern import FilterAbcdPattern
from testUtil import TestUtil

class TestFilterAbcdPattern(unittest.TestCase):

    def testAbcdPattern_01(self):
        seed = [23, 22, 21, 20, 21, 22, 23, 24, 25, 24, 23, 22, 23, 24]
        df = TestUtil.dfSetup(seed)
        app = FilterAbcdPattern()
        result = app.Run('AAPL', df, 24.5)
        self.assertEqual(result, True)


    def testAbcdPattern_02(self):
        seed = [23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34]
        df = TestUtil.dfSetup(seed)
        app = FilterAbcdPattern()
        result = app.Run('AAPL', df, 23.5)
        self.assertEqual(result, False)


    def testAbcdPattern_03(self):
        seed = [23, 22, 21, 20, 21, 22, 23, 24, 25, 24, 23, 22, 23, 24]
        df = TestUtil.dfSetup(seed)
        app = FilterAbcdPattern()
        result = app.Run('AAPL', df, 20.5)
        self.assertEqual(result, False)
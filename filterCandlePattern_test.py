from datetime import datetime, timedelta
import unittest
import pandas as pd
from filterCandlePattern import FilterCandlePattern
from testUtil import TestUtil


class TestFilterCandlePattern(unittest.TestCase):

    def testEngulfingPattern_01(self):
        data = [
            {'Close': 24.05, 'Open': 20.50},
            {'Close': 21.00, 'Open': 21.50},
            {'Close': 21.50, 'Open': 22.50},
            {'Close': 22.50, 'Open': 23.50}
            ]
        df = TestUtil.dfSetupOC(data)
        app = FilterCandlePattern()
        result = app.Run('AAPL', df)
        self.assertEqual(result, 1)


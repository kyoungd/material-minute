from datetime import datetime, timedelta
import unittest
import pandas as pd
from filterVolumeSpreadAnalysis import volumeSpreadAnalysis
from testUtil import TestUtil


class TestFilterVolumeSpreadAnalysis(unittest.TestCase):

    def executeApp(self, symbol, endDate, endHour, endMinute, timeframe):
        isOk, df = TestUtil.getRealtimeData(
            symbol, endDate, endHour, endMinute, timeframe)
        app = volumeSpreadAnalysis()
        return app.Run(symbol, df)
    
    def testForMorningStar(self):
        data = [
            {'Open': 24.80, 'Close': 25.20},
            {'Open': 20.88, 'Close': 24.80},
            {'Open': 20.90, 'Close': 21.00},
            {'Open': 25.00, 'Close': 20.90},
            {'Open': 25.50, 'Close': 25.00},
            {'Open': 26.00, 'Close': 25.50},
            {'Open': 26.50, 'Close': 26.00},
            {'Open': 27.00, 'Close': 26.50},
            {'Open': 27.50, 'Close': 27.00},
            {'Open': 27.50, 'Close': 27.00},
            {'Open': 27.50, 'Close': 27.00},
            {'Open': 27.50, 'Close': 27.00},
            {'Open': 27.50, 'Close': 27.00},
            {'Open': 27.50, 'Close': 27.00},
            {'Open': 27.50, 'Close': 27.00},
            {'Open': 27.50, 'Close': 27.00},
            {'Open': 27.50, 'Close': 27.00},
            {'Open': 27.50, 'Close': 27.00},
            {'Open': 27.50, 'Close': 27.00},
            {'Open': 27.50, 'Close': 27.00},
            {'Open': 27.50, 'Close': 27.00},
            {'Open': 27.50, 'Close': 27.00},
            {'Open': 27.50, 'Close': 27.00},
            {'Open': 27.50, 'Close': 27.00},
            {'Open': 27.50, 'Close': 27.00},
            {'Open': 27.50, 'Close': 27.00},
            {'Open': 27.50, 'Close': 27.00},
            {'Open': 27.50, 'Close': 27.00}
        ]
        df = TestUtil.dfSetupOC(data)
        app = volumeSpreadAnalysis()
        result = app.Run('AAPL', df)
        self.assertEqual(result, 11)

    def testForEveningStar(self):
        data = [
            { 'Spread': 0.5, 'Volume': 1 },
            { 'Spread': 3.6, 'Volume': 1 },
            { 'Spread': 0.4, 'Volume': 1 },
            { 'Spread': -4.1, 'Volume': 1 },
            { 'Spread': -0.5, 'Volume': 1 },
            { 'Spread': -0.4, 'Volume': 1 },
            { 'Spread': -0.3, 'Volume': 1 },
            { 'Spread': -0.3, 'Volume': 1 },
            { 'Spread': -0.3, 'Volume': 1 },
            { 'Spread': -0.3, 'Volume': 1 },
            { 'Spread': -0.3, 'Volume': 1 },
            { 'Spread': -0.3, 'Volume': 1 },
            { 'Spread': -0.3, 'Volume': 1 },
            { 'Spread': -0.3, 'Volume': 1 },
            { 'Spread': -0.3, 'Volume': 1 },
            { 'Spread': -0.3, 'Volume': 1 },
            { 'Spread': -0.3, 'Volume': 1 },
            { 'Spread': -0.3, 'Volume': 1 },
            { 'Spread': -0.3, 'Volume': 1 },
            { 'Spread': -0.3, 'Volume': 1 },
            { 'Spread': -0.3, 'Volume': 1 },
            { 'Spread': -0.3, 'Volume': 1 },
            { 'Spread': -0.3, 'Volume': 1 },
            { 'Spread': -0.3, 'Volume': 1 },
            { 'Spread': -0.3, 'Volume': 1 },
            { 'Spread': -0.3, 'Volume': 1 }
        ]
        df = TestUtil.dfSetupVS(data)
        app = volumeSpreadAnalysis()
        result = app.Run('AAPL', df)
        self.assertEqual(result, 11)
        
    def testForDownwardThrust(self):
        data = [
            {'Spread': 0.5, 'Volume': 1},
            {'Spread': -0.02, 'Volume': 5},
            {'Spread': -2, 'Volume': 1.5},
            {'Spread': -1.5, 'Volume': 1.2},
            {'Spread': -1.2, 'Volume': 1.1},
            {'Spread': -0.8, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
        ]
        df = TestUtil.dfSetupVS(data)
        app = volumeSpreadAnalysis()
        result = app.Run('AAPL', df)
        self.assertEqual(result, 1)

    def testForSellingClimax(self):
        data = [
            {'Spread': 0.5, 'Volume': 1},
            {'Spread': -5, 'Volume': 5},
            {'Spread': -2, 'Volume': 1.5},
            {'Spread': -1.5, 'Volume': 1.2},
            {'Spread': -1.2, 'Volume': 1.1},
            {'Spread': -0.8, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
            {'Spread': -0.3, 'Volume': 1},
        ]
        df = TestUtil.dfSetupVS(data)
        app = volumeSpreadAnalysis()
        result = app.Run('AAPL', df)
        self.assertEqual(result, 2)

    def testForPriceSpike(self):
        result = self.executeApp('PBTS', '2022-06-09', 8, 51, '1Min')
        self.assertTrue(result)

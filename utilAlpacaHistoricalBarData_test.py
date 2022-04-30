import unittest
from utilAlpacaHistoricalBarData import AlpacaHistoricalBarData
from alpacaHistorical import TimePeriod


class TestAlpacaHistoricalBarData(unittest.TestCase):
    def setUp(self):
        self.symbol = 'WBD'
        self.timeframe = TimePeriod.Min15.value
        self.starttime = '2022-04-28T00:01:04Z'
        self.endtime = '2022-04-28T15:30:00Z'
        self.app = AlpacaHistoricalBarData(self.symbol, self.starttime, self.endtime, self.timeframe)
        pass

    # https://data.alpaca.markets/v2/stocks/WBD/bars?start=2022-04-28T00:01:04Z&end=2022-04-28T15:30:00Z&timeframe=5Min
    
    def testDownloadBar_01(self):
        isOk, result = self.app.getHistoricalData()
        self.assertTrue(isOk)


    def testDownloadBar_02(self):
        self.app.DeleteFile()
        isOk, result = self.app.GetData()
        self.assertTrue(isOk)
        isExist = self.app.isExist()
        self.assertTrue(isExist)


    def testDowloadBar_03(self):
        isOk, df = self.app.GetDataFrame()
        self.assertTrue(isOk)
        self.assertGreater(len(df), 0)

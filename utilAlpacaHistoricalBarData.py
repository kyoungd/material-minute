import json
import logging
import os.path
import pandas as pd
from alpacaHistorical import AlpacaHistorical, TimePeriod


class AlpacaHistoricalBarData:
    def __init__(self, symbol: str, starttime: str, endtime: str, timeframe: str) -> None:
        self.filename = self.getFileName(symbol, starttime, endtime, timeframe)
        self.symbol = symbol
        self.starttime = starttime
        self.endtime = endtime
        self.timeframe = TimePeriod.Min5.value if timeframe is None else timeframe
        self.data = None
        
    def getFileName(self, symbol: str, starttime: str, endtime: str, timeframe: str) -> list:
        filename = f'./data/bar-{symbol}-{starttime}-{endtime}-{timeframe}.json'
        filename = filename.replace(':', '-')
        return filename

    def isExist(self):
        return os.path.exists(self.filename)
        
    def readJson(self):
        try:
            with open(self.filename, "r") as openfile:
                data = json.load(openfile)
            return data
        except Exception as e:
            logging.error(
                f'JsonFavorite.readJson Error reading json file: {self.filename} {e}')
            print(
                f'JsonFavorite.readJson Error reading json file: {self.filename} {e}')
            raise Exception(e)

    def getHistoricalData(self):
        try:
            historical = AlpacaHistorical()
            result = historical.HistoricalPrices(
                symbol=self.symbol, timeframe=self.timeframe, starttime=self.starttime, endtime=self.endtime)
            return True, result
        except Exception as e:
            print(f'Util.getHistoricalData: {self.symbol} - {e}')
            return False, None

    def WriteJson(self, data=None):
        try:
            data = self.data if data is None else data
            with open(self.filename, "w") as outfile:
                json.dump(data, outfile)
        except Exception as e:
            logging.error(
                f'JsonFavorite.WriteJson Error Writing json file: {self.filename} {e}')
            print(
                f'JsonFavorite.WriteJson Error Writing json file: {self.filename} {e}')
            raise Exception(e)

    def GetData(self):
        if self.data is None:
            if self.isExist():
                self.data = self.readJson()
            else:
                isDownloadOk, self.data = self.getHistoricalData()
                if isDownloadOk:
                    self.WriteJson(self.data)
                else:
                    return False, None
        return True, self.data

    def DeleteFile(self):
        if self.isExist():
            os.remove(self.filename)

    def GetDataFrame(self):
        isOk, data = self.GetData()
        if isOk:
            df = pd.DataFrame(data)
            df.rename(columns={'c': 'Close', 'o': 'Open', 'h': 'High',
                      'l': 'Low', 'v': 'Volume', 't': 'Date'}, inplace=True)
            return True, df
        else:
            return False, None

from datetime import datetime, timedelta
import pandas as pd
from utilAlpacaHistoricalBarData import AlpacaHistoricalBarData

class TestPublisher:
    def __init__(self, callback):
        self.callback = callback

    def publish(self, data):
        self.callback(data)

class TestUtil:

    @staticmethod
    def dfSetup(data:list):
        startdate = datetime.today()
        datagrid = []
        for row in data:
            startdate = startdate - timedelta(days=1)
            item = {
                'Date': startdate.strftime('%Y-%m-%dT00:00:00.000000000'),
                'Close': row,
                'Volume': 10000000,
                'High': row + 0.5,
                'Low': row - 0.5,
                'Open': row - 0.2
            }
            datagrid.append(item)
        df = pd.DataFrame(datagrid)
        return df

    @staticmethod
    def dfSetupOC(data:list):
        startdate = datetime.today()
        datagrid = []
        for row in data:
            startdate = startdate - timedelta(days=1)
            high = max(row['Close'], row['Open'])
            low = min(row['Close'], row['Open'])
            item = {
                'Date': startdate.strftime('%Y-%m-%dT00:00:00.000000000'),
                'Close': row['Close'],
                'Volume': 10000000,
                'High': high + 0.5,
                'Low': low - 0.5,
                'Open': row['Open']
            }
            datagrid.append(item)
        df = pd.DataFrame(datagrid)
        return df
    
    
    @staticmethod
    def dfSetupVS(data:list, open: float = None) -> pd.DataFrame:
        startdate = datetime.today()
        volume = 1000000
        open = 50 if open is None else open
        datagrid = []
        for row in data:
            startdate = startdate - timedelta(days=1)
            close = open
            open += row['Spread']
            high = max(open, close) + 0.4
            low = min(open, close) - 0.4
            item = {
                'Date': startdate.strftime('%Y-%m-%dT00:00:00.000000000'),
                'Close': close,
                'Volume': volume * row['Volume'],
                'High': high + 0.5,
                'Low': low - 0.5,
                'Open': open
            }
            datagrid.append(item)
        df = pd.DataFrame(datagrid)
        return df

    @staticmethod
    def getYesterday(endDate:str) -> str:
        today = datetime.strptime(endDate, '%Y-%m-%d')
        yesterday = today - timedelta(days=1)
        return yesterday.strftime('%Y-%m-%d')
    
    @staticmethod
    def getRealtimeData(symbol:str, endDate:str, endHour:int, endMinute:int, timeframe:str):
        yesterday = TestUtil.getYesterday(endDate)
        starttime = f'{yesterday}T11:30:00Z'
        ehour = '{0:02d}'.format(endHour+7)
        eminute = '{0:02d}'.format(endMinute)
        endtime = f'{endDate}T{ehour}:{eminute}:00Z'
        app = AlpacaHistoricalBarData(symbol, starttime, endtime, timeframe)
        return app.GetDataFrame()

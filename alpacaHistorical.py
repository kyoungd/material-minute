from alpaca_trade_api.rest import REST, TimeFrame
from datetime import datetime, timedelta
from enum import Enum
import alpaca_trade_api as tradeapi
import requests
from redisUtil import TimeStamp, AlpacaAccess, RedisTimeFrame
import json

custom_header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
response = requests.get('https://www.dev2qa.com', headers=custom_header)


class TimePeriod(Enum):
    REALTIME = "0"
    Min1 = "1Min"
    Min2 = "2Min"
    Min5 = "5Min"
    Min10 = "10Min"
    Min15 = "15Min"
    Min30 = "30Min"
    Hour = "Hour"
    Hour4 = "4Hour"
    Day = "Day"
    Week = "Week"


class AlpacaHistorical:
    ALPACA_URL = 'https://data.alpaca.markets/v2/stocks/%s/bars?start=%s&end=%s&timeframe=%s'
    conn: REST = None

    def __init__(self):
        self.custom_header = AlpacaAccess.CustomHeader()

    def timeframe_start(self, timeframe):
        switcher = {
            RedisTimeFrame.REALTIME: datetime.now() - timedelta(minutes=30),
            RedisTimeFrame.MIN1: datetime.now() - timedelta(minutes=30),
            RedisTimeFrame.MIN2: datetime.now() - timedelta(minutes=60),
            RedisTimeFrame.MIN5: datetime.now() - timedelta(minutes=150),
            RedisTimeFrame.MIN15: datetime.now() - timedelta(minutes=450),
            RedisTimeFrame.MIN30: datetime.now() - timedelta(days=2),
            RedisTimeFrame.HOUR: datetime.now() - timedelta(days=28),
            RedisTimeFrame.DAILY: datetime.now() - timedelta(days=360),
            RedisTimeFrame.WEEKLY: datetime.now() - timedelta(days=1080),
        }
        dt = switcher.get(timeframe, datetime.now())
        date_string = dt.isoformat('T') + 'Z'
        return date_string
        # return "2021-02-08"

    def timeframe_end(self, timeframe):
        dt = datetime.now()
        date_string = dt.isoformat('T') + 'Z'
        return date_string
        # return "2021-02-10"

    def columnName(self, datatype):
        switcher = {
            "open": "o",
            "close": "c",
            "high": "h",
            "low": "l",
            "volume": "v"
        }
        return switcher.get(datatype, 'c')

    def reverseArray(self, arrayData):
        return arrayData[::-1]

    def column(self, matrix, i):
        return [row[i] for row in matrix]

    def adjustPrices(self, data, datatype):
        result = json.loads(data.text)
        bars = result['bars']
        if bars is None:
            return []
        data = self.reverseArray(bars)
        if datatype is None:
            return data
        else:
            dtype = self.columnName(datatype)
            prices = self.column(data, dtype)
            return prices

    def HistoricalPrices(self, symbol, timeframe, datatype=None, starttime=None, endtime=None):
        start = self.timeframe_start(
            timeframe) if starttime is None else starttime
        end = self.timeframe_end(timeframe) if endtime is None else endtime
        tf = '1Min' if RedisTimeFrame.REALTIME == timeframe else timeframe
        url = AlpacaHistorical.ALPACA_URL % (
            symbol, start, end, tf)
        data = requests.get(url, headers=self.custom_header)
        bars = self.adjustPrices(data, datatype)
        return bars

from redisTimeseriesData import ComposeData, RealTimeBars
from redistimeseries.client import Client
from redisUtil import RedisTimeFrame, TimeStamp
from RedisTimeseriesTable import TimeseriesTable
from redisUtil import bar_key, TimeStamp, RedisTimeFrame, TimeSeriesAccess, AlpacaAccess
from unittest import mock
import json
import time


rts = None
symbol = None
rtb = None


def setup_function(module):
    """
    Setup the test function
    """
    app = TimeseriesTable()
    app.ClearAll()
    app.CreateRedisStockSymbol(["TEST"])
    global rts
    rts = TimeSeriesAccess.connection()
    global symbol
    symbol = "TEST"
    global rtb
    rtb = RealTimeBars()


def test_compose_data1():
    """
    Test the compose_data function
    """
    compose_data = ComposeData()
    data1 = [(1300, 1), (1240, 2), (1120, 4), (1060, 5), (1000, 6)]
    ts = 1300
    timeframe = RedisTimeFrame.MIN1

    bar1 = compose_data.AdjustBars(data1, timeframe, ts)
    data2 = [(1300, 1), (1240, 2), (1180, 4), (1120, 4), (1060, 5)]
    assert bar1 == data2


def test_compose_data2():
    """
    Test the compose_data function
    """
    compose_data = ComposeData()
    data1 = [(1600, 1), (1480, 2), (1240, 4), (1120, 5), (1000, 6)]
    ts = 1600
    timeframe = RedisTimeFrame.MIN2

    bar1 = compose_data.AdjustBars(data1, timeframe, ts)
    data2 = [(1600, 1), (1480, 2), (1360, 4), (1240, 4), (1120, 5)]
    assert bar1 == data2


def test_realtimeDataMinutes():
    """
    Test the RedisGetRealtimeData function
    """
    timeframe = RedisTimeFrame.MIN1
    seconds = 60 * 1
    ts = 1000
    rts.add(bar_key(symbol, "close", timeframe), ts, 10.0)
    rts.add(bar_key(symbol, "close", timeframe), ts + seconds, 10.0)
    rts.add(bar_key(symbol, "close", timeframe), ts + 2*seconds, 10.0)
    rts.add(bar_key(symbol, "close", timeframe), ts + 3*seconds, 10.0)
    rts.add(bar_key(symbol, "close", timeframe), ts + 4*seconds, 10.0)
    #
    sample = [
        {'t': ts + 4*seconds, 'c': 10, 'o': 10, 'h': 10, 'l': 10, 'v': 10},
        {'t': ts + 3*seconds, 'c': 10, 'o': 10, 'h': 10, 'l': 10, 'v': 10},
        {'t': ts + 2*seconds, 'c': 10, 'o': 10, 'h': 10, 'l': 10, 'v': 10},
        {'t': ts + 1*seconds, 'c': 10, 'o': 10, 'h': 10, 'l': 10, 'v': 10},
        {'t': ts + 0*seconds, 'c': 10, 'o': 10, 'h': 10, 'l': 10, 'v': 10}
    ]
    #
    rts.add(bar_key(symbol, "open", timeframe), ts, 10.0)
    rts.add(bar_key(symbol, "open", timeframe), ts + seconds, 10.0)
    rts.add(bar_key(symbol, "open", timeframe), ts + 2*seconds, 10.0)
    rts.add(bar_key(symbol, "open", timeframe), ts + 3*seconds, 10.0)
    rts.add(bar_key(symbol, "open", timeframe), ts + 4*seconds, 10.0)
    #
    rts.add(bar_key(symbol, "high", timeframe), ts, 10.0)
    rts.add(bar_key(symbol, "high", timeframe), ts + seconds, 10.0)
    rts.add(bar_key(symbol, "high", timeframe), ts + 2*seconds, 10.0)
    rts.add(bar_key(symbol, "high", timeframe), ts + 3*seconds, 10.0)
    rts.add(bar_key(symbol, "high", timeframe), ts + 4*seconds, 10.0)
    #
    rts.add(bar_key(symbol, "low", timeframe), ts, 10.0)
    rts.add(bar_key(symbol, "low", timeframe), ts + seconds, 10.0)
    rts.add(bar_key(symbol, "low", timeframe), ts + 2*seconds, 10.0)
    rts.add(bar_key(symbol, "low", timeframe), ts + 3*seconds, 10.0)
    rts.add(bar_key(symbol, "low", timeframe), ts + 4*seconds, 10.0)
    #
    rts.add(bar_key(symbol, "volume", timeframe), ts, 10.0)
    rts.add(bar_key(symbol, "volume", timeframe), ts + seconds, 10.0)
    rts.add(bar_key(symbol, "volume", timeframe), ts + 2*seconds, 10.0)
    rts.add(bar_key(symbol, "volume", timeframe), ts + 3*seconds, 10.0)
    rts.add(bar_key(symbol, "volume", timeframe), ts + 4*seconds, 10.0)
    #
    data = rtb.realtimeDataMinutes(
        rts, symbol, timeframe, ts, ts + 4*seconds)
    assert data == sample


@mock.patch('redisTimeseriesData.RealTimeBars._bar_historical',
            return_value=[{'t': 1000, 'c': 10.0, 'o': 10.0, 'h': 10.0, 'l': 10.0, 'v': 10.0}])
def test_realtimeDataMinutesComplete(callHistory):
    timeframe = RedisTimeFrame.MIN1
    seconds = 60 * 1
    ts = 1000
    result = rtb.realtimeDataMinutesComplete(
        rts, symbol, timeframe, ts, ts + 4*seconds)
    assert result == [{'t': 1000, 'c': 10.0,
                       'o': 10.0, 'h': 10.0, 'l': 10.0, 'v': 10.0}]


def test_realtimeDataHistorical():
    startt = 1612166400
    endt = 1612684800
    timeframe = RedisTimeFrame.DAILY
    data = rtb.realtimeDataHistorical(
        rts, 'MSFT', timeframe, startt, endt)
    print(data)
    sample = [{"t": "2021-02-05T05:00:00Z", "o": 242.36, "h": 243.28, "l": 240.42, "c": 242.2, "v": 18055355, "n": 218268, "vw": 241.728827}, {"t": "2021-02-04T05:00:00Z", "o": 242.76, "h": 243.2399, "l": 240.37, "c": 242.01, "v": 25296111, "n": 269886, "vw": 241.458344}, {
        "t": "2021-02-03T05:00:00Z", "o": 239.8, "h": 245.09, "l": 239.26, "c": 243, "v": 27158104, "n": 289329, "vw": 242.771049}, {"t": "2021-02-02T05:00:00Z", "o": 241.06, "h": 242.31, "l": 238.69, "c": 239.51, "v": 25925275, "n": 299119, "vw": 240.268236}, {"t": "2021-02-01T05:00:00Z", "o": 235.16, "h": 242.5, "l": 232.43, "c": 239.65, "v": 33315153, "n": 401535, "vw": 238.758565}]
    assert data == sample


def test_realtimeAddSecond():
    time.sleep(5)
    data = {'symbol': symbol,
            'close': 12.01, 'volume': 1000}
    for ix in range(0, 60):
        rtb.RedisAddTrade(data)
        rtb.RedisAddTrade(data)
        rtb.RedisAddTrade(data)
        time.sleep(1)
    timeframe = RedisTimeFrame.REALTIME
    result = rtb.RedisGetRealtimeData(None, symbol, timeframe)
    assert result['data'][0]['c'] == 12.01

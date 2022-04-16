import logging
import sys
import json
from datetime import datetime
import time
from redisHash import ActiveBars
from redisTimeseriesData import RealTimeBars
from RedisTimeseriesTable import TimeseriesTable
from redis3barScore import StudyThreeBarsScore
from redisPubsub import RedisPublisher
from pubsubKeys import PUBSUB_KEYS
from redisUtil import SetInterval


def barData(open, close, high, low, volume, symbol, change):
    bar = {
        'o': open + change,
        'c': close + change,
        'h': high + change,
        'l': low + change,
        'v': volume,
        'S': symbol,
    }
    return bar


bars2Min = []
bars5Min = []


def create2MinBars(symbol):
    open = 10.10
    close = 10.00
    high = 10.30
    low = 9.05
    change = 0
    bars2Min.append(barData(open, close, high, low, 2700000, symbol, change))
    bars2Min.append(barData(open, close, high, low, 2700000, symbol, change))
    change = 1.00
    bars2Min.append(barData(open, close, high, low, 2700000, symbol, change))
    bars2Min.append(barData(open, close, high, low, 2700000, symbol, change))
    # start 4 bar play
    bars2Min.append(barData(open, close, high, low, 2700000, symbol, change))
    bars2Min.append(barData(open, close, high, low, 2700000, symbol, change))
    # end of 4 bar play
    change = 0.50
    bars2Min.append(barData(open, close, high, low, 2700000, symbol, change))
    bars2Min.append(barData(open, close, high, low, 2700000, symbol, change))


def getNext2MinBar(symbol):
    if len(bars2Min) > 0:
        bar = bars2Min.pop(0)
        return bar
    else:
        create2MinBars(symbol)
        return bars2Min.pop(0)


def create5MinBars(symbol):
    open = 10.10
    close = 10.00
    high = 10.30
    low = 10.05
    change = 0
    bars5Min.append(barData(open, close, high, low, 2700000, symbol, change))
    bars5Min.append(barData(open, close, high, low, 2700000, symbol, change))
    bars5Min.append(barData(open, close, high, low, 2700000, symbol, change))
    bars5Min.append(barData(open, close, high, low, 2700000, symbol, change))
    bars5Min.append(barData(open, close, high, low, 2700000, symbol, change))
    change = 1.00
    bars5Min.append(barData(open, close, high, low, 2700000, symbol, change))
    bars5Min.append(barData(open, close, high, low, 2700000, symbol, change))
    bars5Min.append(barData(open, close, high, low, 2700000, symbol, change))
    bars5Min.append(barData(open, close, high, low, 2700000, symbol, change))
    bars5Min.append(barData(open, close, high, low, 2700000, symbol, change))
    change = 0.50
    bars5Min.append(barData(open, close, high, low, 2700000, symbol, change))
    bars5Min.append(barData(open, close, high, low, 2700000, symbol, change))
    bars5Min.append(barData(open, close, high, low, 2700000, symbol, change))
    bars5Min.append(barData(open, close, high, low, 2700000, symbol, change))
    bars5Min.append(barData(open, close, high, low, 2700000, symbol, change))


def getNext5MinBar(symbol):
    if len(bars5Min) > 0:
        bar = bars5Min.pop(0)
        return bar
    else:
        create5MinBars(symbol)
        return bars5Min.pop(0)


rtb: RealTimeBars = RealTimeBars()
ab: ActiveBars = ActiveBars()
process = StudyThreeBarsScore()


publisherTrade: RedisPublisher = RedisPublisher(PUBSUB_KEYS.EVENT_TRADE_NEW)


def TradeBar(symbol: str):
    data = {'symbol': symbol,
            'close': 10.45, 'volume': 70000}
    logging.info(f'TRADE: {data}')
    publisherTrade.publish(data)


class DictObj:
    def __init__(self, in_dict: dict):
        assert isinstance(in_dict, dict)
        for key, val in in_dict.items():
            if isinstance(val, (list, tuple)):
                setattr(self, key, [DictObj(x) if isinstance(
                    x, dict) else x for x in val])
            else:
                setattr(self, key, DictObj(val)
                        if isinstance(val, dict) else val)


def rfc3339timestamp():
    seconds = time.time()
    # return datetime.utcnow().isoformat() + 'Z'
    # time.time_ns()
    # seconds = time.time_ns() / 1000
    # seconds = seconds / 1000
    # seconds = seconds / 1000
    ts = {"seconds": int(seconds)}
    # dict to object
    return DictObj(ts)


publisher: RedisPublisher = RedisPublisher(PUBSUB_KEYS.EVENT_BAR_CANDIDATE)


def MinInterval(symbol, period):
    print('MinAlert - ')
    if (period == '2MIN'):
        print('min-interval: 2MIN ')
        bar = getNext2MinBar(symbol)
    else:
        print('min-interval: 5MIN ')
        bar = getNext5MinBar(symbol)
    bar['t'] = rfc3339timestamp()
    seconds = bar['t'].seconds
    bar['t'] = seconds
    print('bar', bar)
    publisher.publish(bar)
    # rtb.RedisAddBar(bar)
    # ab.addSymbol(bar['S'])


if __name__ == '__main__':
    symbol = "FANG"
    period = "2MIN"

    args = sys.argv[1:]
    if len(args) > 0 and (args[0] == "-t" or args[0] == "-table"):
        app = TimeseriesTable()
        app.CreateRedisStockSymbol([symbol])

    test = rfc3339timestamp()
    # parameter parsing
    print('starting.  please stand by.  It might take a minute or two to start')
    obj_now = datetime.now()
    secWait = 60 - obj_now.second
    time.sleep(secWait)

    print('starting 1 minute data cycle.')
    SetInterval(60, lambda: MinInterval(symbol, period))
    SetInterval(5, lambda: TradeBar(symbol))

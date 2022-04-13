from redisHash import StoreStack, StoreTradeSubscription, StoreScore
from RedisTimeseriesTable import TimeseriesTable


def setup_function(module):
    """
    Setup the test function
    """
    app = TimeseriesTable()
    app.ClearAll()
    global symbol
    symbol = "TEST"


def test_StoreStack():
    """
    Test StoreStack
    """
    stack = StoreStack()
    data1 = {'data': 2}
    stack.add(symbol, data1)
    data2 = stack.value(symbol)
    assert data1 == data2


def test_StoreTradeSubscription():
    """
    Test StoreTradeSubscription
    """
    trade = StoreTradeSubscription()
    data1 = {'data': 2}
    trade.add(symbol, data1)
    data2 = trade.value(symbol)
    assert data1 == data2


def test_StoreScore():
    """
    Test StoreScore
    """
    score = StoreScore()
    data1 = {'data': 2}
    score.add(symbol, data1)
    data2 = score.value(symbol)
    assert data1 == data2

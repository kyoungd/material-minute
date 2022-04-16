from redis3barScore import StudyThreeBarsScore
from redisUtil import RedisTimeFrame


def test_score1() -> None:
    package = {'close': 13.92,
               'high': 14.57,
               'low': 12.45,
               'open': 13.4584,
               'symbol': 'FANG',
               'timestamp': 1627493640000000000,
               'trade_count': 602,
               'volume': 213907,
               'vwap': 8.510506}
    app = StudyThreeBarsScore()
    newPrice = 13.70
    realtime = []
    symbol = "FANG"
    stack = {'symbol': symbol, 'value': {
        'firstPrice': 13.50,
        'secondPrice': 14.00,
        'thirdPrice': 13.00,
        'timeframe': RedisTimeFrame.MIN2
    }}
    score1 = app.ThreeBarPlay(13.60, [], stack)
    assert score1 == 4

    score2 = app.ThreeBarPlay(13.40, [], stack)
    assert score2 == 2

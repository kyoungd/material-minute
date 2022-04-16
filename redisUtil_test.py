from redisUtil import bar_key, AlpacaAccess, AlpacaStreamAccess, RedisAccess, RedisTimeFrame, TimeStamp
from unittest import mock


def test_bar_key() -> None:
    """generate redis time serires table name for bar data"""
    assert bar_key('SYMB', "close", "1Min") == "data_close_1MIN:SYMB"


def test_AlpacaAccess() -> None:
    """test AlpacaAccess class"""
    access = AlpacaAccess.connection()
    assert access is not None


def test_AlpacaStreamAccess() -> None:
    """test AlpacaStreamAccess class"""
    access = AlpacaStreamAccess.connection()
    assert access is not None


def test_RedisAccess() -> None:
    """test RedisAccess class"""
    access = RedisAccess.connection()
    assert access is not None


@mock.patch('redisUtil.TimeStamp.now', return_value=0)
def test_get_start_time(now) -> None:
    """test get_start_time method"""
    assert TimeStamp.get_starttime(
        RedisTimeFrame.MIN1) == TimeStamp.getStartTime(RedisTimeFrame.MIN1)

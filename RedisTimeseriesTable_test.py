from RedisTimeseriesTable import TimeseriesTable
from unittest import mock


def test_timeseriesTableCheck() -> None:
    app = TimeseriesTable()
    app.RemoveStock("TEST")
    app.CreateRedisStockSymbol(["TEST"])
    assert app.CheckRedisStockSymbol("TEST") == True

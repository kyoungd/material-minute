##
# Create various Redis TimeSeries for storing stock prices
# and technical indicators
# Author: Prasanna Rajagopal
##

import alpaca_trade_api as alpaca
from alpaca_trade_api.rest import TimeFrame
from datetime import datetime, timedelta
from redisUtil import RedisAccess, TimeStamp, bar_key, RedisTimeFrame, AlpacaAccess, TimeSeriesAccess, KeyName
from redistimeseries.client import Client


# def bar_key(symbol, suffix, time_frame):
#     return "data_" + suffix + "_" + time_frame + ":" + symbol


class TimeseriesTable:
    isAutoAggregate = False

    def __init__(self, rts=None):
        self.rts = TimeSeriesAccess.connection(rts)
        self.redis = RedisAccess.connection()
        api = AlpacaAccess.connection()
        self.assets = api.list_assets(status='active')

    def addSymbolItem(self, rts, symbol, suffix, aggr, index, description, companyName, timeframe, duppolicy=None):
        name0 = bar_key(symbol, suffix, timeframe)
        retention = TimeStamp.retention_in_ms(timeframe)
        labels0 = {'SYMBOL': symbol, 'DESC': 'RELATIVE_STRENGTH_INDEX', 'INDEX': 'DJIA',
                   'TIMEFRAME': timeframe, 'INDICATOR': aggr}
        if duppolicy is not None:
            rts.create(name0, retention_msecs=retention,
                       labels=labels0, duplicate_policy=duppolicy)
        else:
            rts.create(name0, retention_msecs=retention,
                       labels=labels0)
        return name0

    def addSymbol(self, rts, symbol, suffix, aggr, index, description, companyName):
        if suffix == 'close' or suffix == 'volume':
            aggr = 'last' if suffix == 'close' else 'sum'
            name0 = self.addSymbolItem(rts, symbol, suffix, aggr,
                                       index, description, companyName, RedisTimeFrame.REALTIME, aggr)
            name10s = self.addSymbolItem(rts, symbol,  suffix, aggr,
                                         index, description, companyName, RedisTimeFrame.SEC10, aggr)
            rts.createrule(name0, name10s, aggr, 10*1)
        name1 = self.addSymbolItem(rts, symbol, suffix, aggr,
                                   index, description, companyName, RedisTimeFrame.MIN1)
        name2 = self.addSymbolItem(rts, symbol, suffix, aggr,
                                   index, description, companyName, RedisTimeFrame.MIN2)
        name5 = self.addSymbolItem(rts, symbol, suffix, aggr,
                                   index, description, companyName, RedisTimeFrame.MIN5)
        name5 = self.addSymbolItem(rts, symbol, suffix, aggr,
                                   index, description, companyName, RedisTimeFrame.MIN15)
        # rts.createrule(name0, name1, aggr, 60*1000)
        if TimeseriesTable.isAutoAggregate:
            rts.createrule(name1, name2, aggr, 2*60)
            rts.createrule(name1, name5, aggr, 5*60)
            rts.createrule(name1, name5, aggr, 15*60)

    def addRedisStockSymbol(self, rts, symbol, index, description, companyName):
        self.addSymbol(rts, symbol, "high", "max",
                       index, description, companyName)
        self.addSymbol(rts, symbol, "low", "min",
                       index, description, companyName)
        self.addSymbol(rts, symbol, "open", "first",
                       index, description, companyName)
        self.addSymbol(rts, symbol, "close", "last",
                       index, description, companyName)
        self.addSymbol(rts, symbol, "volume", "sum",
                       index, description, companyName)

    def CreateRedisStockSymbol(self, symbols):
        for symbol in symbols:
            print(f"{symbol}  \t{symbol}")
            name0 = bar_key(symbol, 'close', RedisTimeFrame.MIN1)
            if not self.redis.exists(name0):
                self.addRedisStockSymbol(
                    self.rts, symbol, '', '', 'SYMBOL-' + symbol)

    def run(self):
        for asset in self.assets:
            print(f"{asset.symbol}  \t{asset.name}")
            self.addRedisStockSymbol(
                self.rts, asset.symbol, '', '', asset.name)

    def deleteRedisSymbol(self, rts, symbol, timeframe):
        name0 = bar_key(symbol, 'close', timeframe)
        if self.redis.exists(name0):
            self.redis.delete(name0)
        name1 = bar_key(symbol, 'open', timeframe)
        if self.redis.exists(name1):
            self.redis.delete(name1)
        name2 = bar_key(symbol, 'high', timeframe)
        if self.redis.exists(name2):
            self.redis.delete(name2)
        name3 = bar_key(symbol, 'low', timeframe)
        if self.redis.exists(name3):
            self.redis.delete(name3)
        name4 = bar_key(symbol, 'volume', timeframe)
        if self.redis.exists(name4):
            self.redis.delete(name4)

    def deleteRedisStockSymbol(self, rts, symbol):
        self.deleteRedisSymbol(rts, symbol, RedisTimeFrame.REALTIME)
        self.deleteRedisSymbol(rts, symbol, RedisTimeFrame.SEC10)
        self.deleteRedisSymbol(rts, symbol, RedisTimeFrame.MIN1)
        self.deleteRedisSymbol(rts, symbol, RedisTimeFrame.MIN2)
        self.deleteRedisSymbol(rts, symbol, RedisTimeFrame.MIN5)
        self.deleteRedisSymbol(rts, symbol, RedisTimeFrame.MIN15)

    def RemoveStock(self, symbol):
        self.deleteRedisStockSymbol(self.rts, symbol)
        if self.redis.exists(KeyName.KEY_THREEBARSTACK):
            self.redis.delete(KeyName.KEY_THREEBARSTACK)
        if self.redis.exists(KeyName.KEY_THREEBARSCORE):
            self.redis.delete(KeyName.KEY_THREEBARSCORE)

    def ClearAll(self):
        self.redis.flushall()

    def checkRedisSymbol(self, rts, symbol, timeframe):
        return self.redis.exists(bar_key(symbol, 'close', timeframe)) or self.redis.exists(bar_key(symbol, 'open', timeframe)) or self.redis.exists(bar_key(symbol, 'high', timeframe)) or self.redis.exists(bar_key(symbol, 'low', timeframe)) or self.redis.exists(bar_key(symbol, 'volume', timeframe))

    def CheckRedisStockSymbol(self, symbol):
        return self.checkRedisSymbol(self.rts, symbol, RedisTimeFrame.REALTIME) or self.checkRedisSymbol(self.rts, symbol, RedisTimeFrame.SEC10) or self.checkRedisSymbol(self.rts, symbol, RedisTimeFrame.MIN1) or self.checkRedisSymbol(self.rts, symbol, RedisTimeFrame.MIN2) or self.checkRedisSymbol(self.rts, symbol, RedisTimeFrame.MIN5)


if __name__ == "__main__":
    app = TimeseriesTable()
    app.run()

from logging import Formatter
from redisPubsub import RedisPublisher
import redis
import json
from redisUtil import KeyName, RedisAccess, StudyScores
from operator import itemgetter
from pubsubKeys import PUBSUB_KEYS

# Redis hash key name.
# this class encapsuates the redis hash operations.
#


class RedisHash:

    def __init__(self, key: str, r=None, callback=None):
        self.redis = RedisAccess.connection(r)
        self.callback = callback
        self.key = key

    # return Hash Key
    @property
    def get_key(self):
        return self.key

    # return all hash fields/values for the given key
    def _getAll(self, key):
        return self.redis.hgetall(key)

    # clean up _getAll()
    def getAll(self):
        return self._getAll(self.key)

    # return all fields for the key
    # redis returns array of byte array.
    # encode it to standard string.
    #
    def getAllSymbols(self):
        arrayOfByteArray = self.redis.hkeys(self.key)
        result = []
        for item in arrayOfByteArray:
            result.append(item.decode('utf-8'))
        return result

    # add a new field/value pair to the hash
    def _add(self, key, symbol, jsondata):
        data = json.dumps(jsondata)
        self.redis.hset(key, symbol, data)
        if (self.callback != None):
            self.callback(symbol, jsondata)

    # clean up _add()
    def add(self, symbol, jsondata):
        return self._add(self.key, symbol, jsondata)

    # delete a field/value pair from the hash key
    def delete(self, symbol):
        self.redis.hdel(self.key, symbol)

    # return value from redish hash key field

    def _value(self, key, symbol):
        data = self.redis.hget(key, symbol)
        if data == None:
            return None
        return json.loads(data)

    # clean up _value()
    def value(self, symbol):
        return self._value(self.key, symbol)

    # does a field exists in the hash key
    def isSymbolExist(self, symbol):
        return self.redis.hexists(self.key, symbol)


# This class encapsulates the Stack Store function.
# It also handles subscribe/unsubscribe to alpaca stream list.
# When a list of subscribe/unsubscribe is created, it published it to redis.
class StoreStack(RedisHash):
    def __init__(self, r=None, unsubCallback=None, key=None):
        if key is None:
            key = KeyName.KEY_THREEBARSTACK
        super().__init__(key, r)
        self.publisher = RedisPublisher(
            channels=KeyName.EVENT_NEW_CANDIDATES, r=self.redis)


class StoreTradeSubscription(RedisHash):
    def __init__(self, r=None, key=None):
        if key is None:
            key = KeyName.KEY_TRADE_SUBSCRIPTION
        super().__init__(key, r)

    def set(self, symbol):
        jsondata = {}
        self.add(symbol, jsondata)

    def remove(self, symbol):
        self.delete(symbol)

# This class encapsulates the Study Scores function.
# It encapsulates redis hash key Score.
#


class StoreScore (RedisHash):
    def __init__(self, r=None, key=None):
        if key is None:
            key = KeyName.KEY_THREEBARSCORE
        super().__init__(key, r)

# This is the Active Bar.  This is the list of one minute stock bar that was updated recently.
# We are only interested in symbols in this list as we only focus on moving stock.


class ActiveBars (RedisHash):

    def __init__(self, r=None):
        super().__init__(key=KeyName.VARIABLE_ACTIVE_BARS, r=r)

    def addSymbol(self, symbol):
        if (not self.isSymbolExist(symbol)):
            self.add(symbol, [])

    def deleteSymbol(self, symbol):
        if (self.isSymbolExist(symbol)):
            self.delete(symbol)

    def deleteAll(self, allsymbols):
        for symbol in allsymbols:
            if (self.isSymbolExist(symbol)):
                self.delete(symbol)


if __name__ == "__main__":
    # app = ActiveBars()
    # app.addSymbol('AAPL')
    # app.addSymbol('GOOG')
    # app.addSymbol('MSFT')
    # app.addSymbol('FB')
    # app.addSymbol('AMZN')
    # symbols = app.getAllSymbols()
    # print(symbols)
    # app.deleteAll(symbols)
    # symbols = app.getAllSymbols()
    # print(symbols)

    app = StoreScore('test')
    app.score.Score = 50
    print(app.score)
    app.save()
    bpp = StoreScore('test')
    bpp.load()
    print(bpp.score)
    #
    #
    # app = StoreStack()
    # app.add("AAPL", {'name': 'test', 'data': 'this is text'})
    # myDict = app.redis.hvals('STUDYTHREEBARSTACK')
    # newDict = []
    # for item in myDict:
    #     print(item)
    # data1 = app.value('FANG')
    # print(app.value("AAPL"))
    # print('done')

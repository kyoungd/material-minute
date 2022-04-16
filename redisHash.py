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
    def Add(self, symbol, jsondata):
        return self._add(self.key, symbol, jsondata)

    # delete a field/value pair from the hash key
    def Delete(self, symbol):
        self.redis.hdel(self.key, symbol)

    # return value from redish hash key field

    def _value(self, key, symbol):
        data = self.redis.hget(key, symbol)
        if data == None:
            return None
        return json.loads(data)

    # clean up _value()
    def Get(self, symbol):
        return self._value(self.key, symbol)

    # does a field exists in the hash key
    def IsSymbolExist(self, symbol):
        return self.redis.hexists(self.key, symbol)

    def deleteAll(self):
        if self.redis.hlen(self.key) > 0:
            self.redis.delete(self.key)


class PivotPointStack(RedisHash):
    def __init__(self):
        key = "HASH_PIVOT_POINTS"
        super().__init__(key)
    
    def Reset(self):
        self.deleteAll()


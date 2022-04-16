import logging
import sys
import json
import time
from redisHash import StoreTradeSubscription
from redisPubsub import RedisPublisher, RedisSubscriber
from pubsubKeys import PUBSUB_KEYS


publisher = RedisPublisher(PUBSUB_KEYS.EVENT_TRADE_SUBSCRIBE)
symbol = 'TSLA'
while 1:
    time.sleep(10)
    data = {"symbol": symbol,
            "operation": "SUBSCRIBE"}
    print('subscribe ', symbol)
    publisher.publish(data)
    time.sleep(10)
    data = {"symbol": symbol,
            "operation": "UNSUBSCRIBE"}
    print('unsubscribe ', symbol)
    publisher.publish(data)

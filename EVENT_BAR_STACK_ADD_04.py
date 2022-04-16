import copy
import logging
from redisPubsub import RedisPublisher, RedisSubscriber
from pubsubKeys import PUBSUB_KEYS
from redisUtil import SetInterval

class RedisStack:
    stack = []
    stackCount = 0
    stackLock1 = False
    stackLock2 = False

    def __init__(self):
        # StoreStack: class to access the redis Stack.
        self.subscriber = RedisSubscriber(
            PUBSUB_KEYS.EVENT_BAR_STACK_ADD, None, self.addStack)
        self.publisher = RedisPublisher(
            PUBSUB_KEYS.EVENT_BAR_POST_TO_SERVER)

    def sendStack(self):
        stackSize = len(RedisStack.stack)
        if stackSize <= 0:
            return
        if RedisStack.stackCount != stackSize:
            RedisStack.stackCount = stackSize
            RedisStack.stackLock1 = False
            RedisStack.stackLock2 = False
        elif RedisStack.stackLock1 and RedisStack.stackLock2:
            self.publisher.publish(RedisStack.stack)
            RedisStack.stack.clear()
            RedisStack.stackCount = 0
            RedisStack.stackLock1 = False
            RedisStack.stackLock2 = False
        elif RedisStack.stackLock1:
            RedisStack.stackLock2 = True
        else:
            RedisStack.stackLock1 = True

    def addStack(self, data):
        RedisStack.stack.append(data)

    def start(self):
        try:
            self.subscriber.start()
            SetInterval(1, self.sendStack)
        except KeyboardInterrupt:
            self.subscriber.stop()
        except Exception as e:
            logging.error(e)

    @staticmethod
    def run():
        logging.info("Starting RedisStack")
        candidate = RedisStack()
        candidate.start()

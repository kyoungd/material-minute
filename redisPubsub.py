import threading
import redis
import logging
import json
from redisTimeseriesData import RealTimeBars
from redisUtil import KeyName, RedisAccess


class RedisSubscriber(threading.Thread):
    def __init__(self, channels, r=None, callback=None):
        threading.Thread.__init__(self)
        self.redis = RedisAccess.connection(r)
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channels)
        self.callback = callback

    def get_redis(self):
        return self.redis

    def work(self, package):
        try:
            if (self.callback == None):
                print(package['channel'], ":", package['data'])
            else:
                data = json.loads(package['data'])
                self.callback(data)
        except Exception as e:
            logging.error(e)

    def run(self):
        for package in self.pubsub.listen():
            if package['data'] == "KILL":
                self.pubsub.unsubscribe()
                print("unsubscribed and finished")
                break
            elif package['type'] == 'message':
                self.work(package)
            else:
                pass


class RedisPublisher:
    def __init__(self, channels, r=None):
        self.redis = RedisAccess.connection(r)
        self.channels = channels

    def publish(self, data):
        package = json.dumps(data)
        self.redis.publish(self.channels[0], package)

    def killme(self):
        self.redis.publish(self.channels[0], 'KILL')


class StreamBarsSubscriber(RedisSubscriber):
    def __init__(self):
        self.rtb = RealTimeBars()
        RedisSubscriber.__init__(self,
                                 KeyName.EVENT_BAR2DB, callback=self.rtb.RedisAddBar)


class StreamBarsPublisher(RedisPublisher):
    def __init__(self):
        RedisPublisher.__init__(self, KeyName.EVENT_BAR2DB)


if __name__ == "__main__":
    pass

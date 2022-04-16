import pandas as pd
import time
import logging
from multiprocessing import Process
from EVENT_APP_VSA_03 import EventBarDataProcess
from EVENT_BAR_STACK_ADD_04 import RedisStack
from EVENT_BAR_POST_TO_SERVER_99 import EventBarPostToServer
from filterFirst import FilterFirst
from redisUtil import RedisTimeFrame
from redisPubsub import RedisSubscriber, RedisPublisher
from pubsubKeys import PUBSUB_KEYS

class RunApp:
    def __init__(self) -> None:
        self.processBars = EventBarDataProcess()
        self.publisher = RedisPublisher(PUBSUB_KEYS.EVENT_BAR_FILTER_VSA)

    def dataSetup(self, p0, p1, p2, p3, p4, p5, v0, v1, v2, v3, v4, v5):
        data = {'Date':
                ['2021-06-07T00:00:00.000000000', '2021-05-01T00:00:00.000000000',
                 '2021-04-12T00:00:00.000000000', '2021-03-23T00:00:00.000000000',
                 '2021-02-28T00:00:00.000000000', '2021-01-01T00:00:00.000000000'],
                'High':
                    [p0+1.01, p1+1.01, p2+1.01,
                     p3+1.01, p4+1.01, p5+1.01],
                'Low':
                    [p0-1.01, p1-1.01, p2-1.01,
                     p3-1.01, p4-1.01, p5-1.01],
                'Open':
                    [p0-0.5, p1-0.5, p2-0.5,
                     p3-0.5, p4-0.5, p5-0.5],
                'Close':
                    [p0+0.1, p1+0.1, p2+0.1,
                     p3+0.1, p4+0.1, p5+0.1],
                'Volume':
                    [v0, v1, v2,
                     v3, v4, v5]
                }
        return data

    def setValues(self, data, index: int, o: float, h: float, l: float, c: float):
        data['High'][index] = h
        data['Low'][index] = l
        data['Open'][index] = o
        data['Close'][index] = c
        return data

    def Run(self):
        symbol = 'AAPL'
        period = RedisTimeFrame.MIN15
        min15data = self.dataSetup(
            0, 0, 0, 60, 66, 70, 200000, 200000, 200000, 200000, 200000, 200000)
        min15data = self.setValues(min15data, 0, 394.480011, 396.720001, 390.750000, 391.480011)
        min15data = self.setValues(min15data, 1, 389.880005, 391.570007, 387.149994, 389.480011)
        min15data = self.setValues(min15data, 2, 390.029999, 394.070007, 389.970001, 392.589996)
        min15data = self.setValues(min15data, 3, 391.910004, 393.459991, 388.660004, 389.500000)
        min15data = self.setValues(min15data, 4, 391.000000, 392.750000, 387.470001, 387.519989)

        data = {'symbol': symbol, 'period': period, 'data': min15data}
        self.publisher.publish(data)


def ThreadRun():
    EventBarDataProcess.run()
    RedisStack.run()
    EventBarPostToServer.run()
    app = RunApp()
    app.Run()
    while 1:
        time.sleep(1)

if __name__ == '__main__':
    formatter = '%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s'
    logging.basicConfig(level=logging.INFO, format=formatter,
                        datefmt='%d-%b-%y %H:%M:%S', filename="three-bar-test.log")
    logging.warning("app.py started")
    ThreadRun()

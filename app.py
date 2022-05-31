import logging
import sys
import time
from datetime import datetime
from multiprocessing import Process
from RedisTimeseriesTable import TimeseriesTable
from EVENT_REALTIME_DATA_01 import RealTimeData
from EVENT_BAR_HANDLE_REALTIME_DATA_02 import EventBarHandleRealtimeData
from EVENT_APP_VSA_03 import EventBarDataProcess
from EVENT_BAR_STACK_ADD_04 import RedisStack
from EVENT_BAR_POST_TO_SERVER_99 import EventBarPostToServer
from redisUtil import SetInterval
from filterPivotPoint import LoadPivotPoints
from utilDailyKeyLevels import DailyKeyLevels


def ThreadRun():
    # multi threading class
    time.sleep(5)  # give the initial connection time to be established
    DailyKeyLevels.run()
    EventBarHandleRealtimeData.run()
    EventBarDataProcess.run()
    RedisStack.run()
    EventBarPostToServer.run()
    while 1:
        time.sleep(1)

def RealtimeApp(isDebug=None):
    isDebug = False if isDebug is None else isDebug
    preprocessing = LoadPivotPoints()
    preprocessing.Run()
    
    if not isDebug:
        p01 = Process(target=RealTimeData)
        p01.start()
    p02 = Process(target=ThreadRun)
    p02.start()
    while 1:
        time.sleep(1)

def RunApp():
    today = datetime.now()
    print(f'{today.hour} {today.minute}')
    if today.hour == 3 and today.minute == 30:
        RealtimeApp()

if __name__ == "__main__":
    formatter = '%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s'
    logging.basicConfig(level=logging.INFO, format=formatter,
                        datefmt='%d-%b-%y %H:%M:%S', filename="three-bar.log")
    logging.warning("app.py started")
    args = sys.argv[1:]
    if len(args) > 0:
        if (args[0] == "--t" or args[0] == "--table"):
            tables = TimeseriesTable()
            tables.run()
        elif (args[0] == "--test"):
            content = [{"datatype": "VSA", "symbol": "AFRM", "timeframe": "5Min", "vsa": 0, "cs": 1, "price": 25.89}, {"datatype": "VSA", "symbol": "MARA", "timeframe": "5Min", "vsa": 0, "cs": 4, "price": 10.5716}, {
                "datatype": "VSA", "symbol": "VTNR", "timeframe": "5Min", "vsa": 0, "cs": 1, "price": 15.75}, {"datatype": "VSA", "symbol": "BWV", "timeframe": "5Min", "vsa": 0, "cs": 1, "price": 5.06}]
            app = EventBarPostToServer()
            app.PushToServer(content)
            RealtimeApp(isDebug=False)
        else:
            RealtimeApp()
    else:
        SetInterval(60, RunApp)
    logging.info('done')

import logging
import requests
import json
from redisPubsub import RedisSubscriber
from pubsubKeys import PUBSUB_KEYS
from environ import EnvFile
from datetime import datetime

class EventBarPostToServer:
    def __init__(self):
        self.subscriber = RedisSubscriber(
            PUBSUB_KEYS.EVENT_BAR_POST_TO_SERVER, None, self.PushToServer)

    def PushToServer(self, content, dest=None, date=None):
        print('start push. current date:')
        print(datetime.now())
        x = filter(lambda x: x['vsa'] > 0 or x['cs'] > 0, content)
        try:
            url = EnvFile.Get(
                'PUSH_REALTIME_URL', 'https://simp-admin.herokuapp.com/api/realtimes?datatype=VSA&timeframe=15Min') if dest is None else dest
            url = url if date is None else url + '&date=' + date
            # url = 'http://localhost:1337/api/realtimes?datatype=VSA&timeframe=15Min'
            data = list(x)
            # if length data > 0
            if len(data) > 0:
                r = requests.post(url, json=data)
                # print(f"Status Code: {r.status_code}, Response: {r.json()}")
                logging.info(f"PushToServer. Status Code: {r.status_code}")
                print(f"PushToServer Status Code: {r.status_code}")
            else:
                logging.info(f"PushToServer. Status Code: 0")
                print(f"PushToServer Status Code: 0")
            # write content to file
            if dest is None:
                with open('./post_to_server.txt', 'a') as f:
                    fdata = json.dumps(data)
                    f.write(datetime.now().strftime("%I:%M%p on %B %d, %Y"))
                    f.write('\n')
                    f.write(fdata)
                    f.write('\n')
        except Exception as e:
            logging.error(f"PushToServer. Exception: {e}")
            print(f"PushToServer. Exception: {e}")

    def start(self):
        try:
            self.subscriber.start()
        except KeyboardInterrupt:
            self.subscriber.stop()
        except Exception as e:
            logging.error(e)

    @staticmethod
    def run():
        logging.info("EVENT_TRADE_ADD.EventBarPostToServer.run")
        candidate = EventBarPostToServer()
        candidate.start()

if __name__ == "__main__":
    # datestr = '05:15AM on May 17, 2022'
    # onedate = datetime.strptime(datestr, '%I:%M%p on %B %d, %Y')
    with open('./post_to_server_bk.txt', 'r') as f:
        fdatalist = f.readlines()
    lineDate = None
    lineJsonData = None
    for row in fdatalist:
        if lineDate is None:
            lineDate = row.replace('\n', '')
        elif lineJsonData is None:
            lineJsonData = row.replace('\n', '')
        if lineDate is not None and lineJsonData is not None:
            onedate = datetime.strptime(lineDate, '%I:%M%p on %B %d, %Y')
            data = json.loads(lineJsonData)
            if len(data) > 0:
                app = EventBarPostToServer()
                app.PushToServer(content=data, date=onedate.strftime(
                    '%Y-%m-%dT%H:%M:%S.000Z'))
                # app.PushToServer(content=data)
            lineDate = None
            lineJsonData = None

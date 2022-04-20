from datetime import datetime, timedelta
import pandas as pd

class TestPublisher:
    def __init__(self, callback):
        self.callback = callback

    def publish(self, data):
        self.callback(data)

class TestUtil:

    @staticmethod
    def dfSetup(data:list):
        startdate = datetime.today()
        datagrid = []
        for row in data:
            startdate = startdate - timedelta(days=1)
            item = {
                'Date': startdate.strftime('%Y-%m-%dT00:00:00.000000000'),
                'Close': row,
                'Volume': 10000000,
                'High': row + 0.5,
                'Low': row - 0.5,
                'Open': row - 0.2
            }
            datagrid.append(item)
        df = pd.DataFrame(datagrid)
        return df


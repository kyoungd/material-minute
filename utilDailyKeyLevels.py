import pandas as pd
import logging
from db import DB
from redisHash import KeyLevelsStack

class DailyKeyLevels:
    def __init__(self):
        self.db = DB()
        self.stack = KeyLevelsStack()
        # if len(DailyKeyLevels.keylevels) <= 0:
        #     levels = self.readAllFromDb()
        #     for row in levels:
        #         try:
        #             symbol = row[0]
        #             data = row[1]
        #             DailyKeyLevels.keylevels[symbol] = data
        #         except Exception as ex:
        #             logging.error(f'DailyKeyLevels.__init__ {row}')

    def readAllFromDb(self):
        query = """SELECT symbol, keylevels FROM public.market_data WHERE timeframe=%s AND NOT is_deleted ORDER BY symbol asc"""
        params = ('1Day',)
        isOk, results = self.db.SelectQuery(query, params)
        if isOk:
            return results
        return None

    def LoadKeyLevels(self):
        self.stack.deleteAll()
        levels = self.readAllFromDb()
        for row in levels:
            try:
                symbol = row[0]
                data = row[1]
                self.stack.Add(symbol, data)
            except Exception as ex:
                logging.error(f'DailyKeyLevels.__init__ {row}')

    @staticmethod
    def run():
        app = DailyKeyLevels()
        app.LoadKeyLevels()
import pandas as pd
import os
from db import DB
import logging
from redisUtil import TimeStamp
from filterPriceSpread import FilterPriceSpread

class FilterDailySupplyDemandZone:
    def __init__(self, marketOpenAt = None):
        self.marketOpenAt = TimeStamp.getMarketOpenTimestamp(
        ) if marketOpenAt is None else marketOpenAt
        self.minMaxRangePercent = 0.06
        self.minMaxNearPercent = 0.04

    def Run(self, symbol: str, df: pd.DataFrame, close: float) -> bool:
        try:
            if len(df) <= 3:
                return False
            high = df['High'].loc[df['High'].idxmax()]
            low = df['Low'].loc[df['Low'].idxmin()]
            if FilterPriceSpread.IsNearPrice(high, close):
                return True
            if FilterPriceSpread.IsNearPrice(low, close):
                return True
            return False
        except Exception as ex:
            logging.error(f'FilterDailySupplyDemandZone {symbol} - {ex}')
            return False


class FilterSupplyDemandZone:
    db:DB = None
    keylevels:dict = {}

    def __init__(self):
        # self.data = [{"Date":"2022-04-07T04:00:00Z","Close":3.86,"Type":"min"},{"Date":"2022-04-01T04:00:00Z","Close":3.9,"Type":"max"},{"Date":"2022-03-18T04:00:00Z","Close":6.41,"Type":"min"},{"Date":"2022-03-14T04:00:00Z","Close":5.29,"Type":"max"},{"Date":"2022-03-09T05:00:00Z","Close":5.93,"Type":"min"},{"Date":"2022-03-04T05:00:00Z","Close":5.02,"Type":"max"},{"Date":"2022-03-02T05:00:00Z","Close":6.13,"Type":"min"},{"Date":"2022-02-24T05:00:00Z","Close":5.38,"Type":"max"},{"Date":"2022-02-22T05:00:00Z","Close":5.93,"Type":"min"},{"Date":"2022-02-14T05:00:00Z","Close":5.13,"Type":"max"},{"Date":"2022-02-09T05:00:00Z","Close":5.8,"Type":"min"},{"Date":"2022-02-04T05:00:00Z","Close":4.76,"Type":"max"},{"Date":"2022-02-01T05:00:00Z","Close":5.22,"Type":"min"},{"Date":"2022-01-28T05:00:00Z","Close":4.81,"Type":"max"},{"Date":"2021-12-31T05:00:00Z","Close":6.96,"Type":"min"},{"Date":"2021-12-29T05:00:00Z","Close":6.56,"Type":"max"},{"Date":"2021-12-22T05:00:00Z","Close":7.12,"Type":"min"},{"Date":"2021-12-14T05:00:00Z","Close":6.54,"Type":"max"},{"Date":"2021-11-05T04:00:00Z","Close":14.96,"Type":"min"},{"Date":"2021-10-19T04:00:00Z","Close":13.46,"Type":"max"},{"Date":"2021-10-14T04:00:00Z","Close":14.5,"Type":"min"},{"Date":"2021-10-11T04:00:00Z","Close":13.09,"Type":"max"},{"Date":"2021-10-04T04:00:00Z","Close":15.37,"Type":"min"},{"Date":"2021-09-28T04:00:00Z","Close":14.7,"Type":"max"},{"Date":"2021-09-24T04:00:00Z","Close":16.14,"Type":"min"},{"Date":"2021-09-21T04:00:00Z","Close":14.73,"Type":"max"},{"Date":"2021-09-08T04:00:00Z","Close":18.52,"Type":"min"},{"Date":"2021-09-02T04:00:00Z","Close":15.27,"Type":"max"},{"Date":"2021-08-31T04:00:00Z","Close":18.96,"Type":"min"},{"Date":"2021-08-04T04:00:00Z","Close":14.65,"Type":"max"},{"Date":"2021-07-30T04:00:00Z","Close":15.48,"Type":"min"},{"Date":"2021-07-27T04:00:00Z","Close":14.5,"Type":"max"},{"Date":"2021-07-20T04:00:00Z","Close":19.11,"Type":"min"},{"Date":"2021-07-16T04:00:00Z","Close":17.17,"Type":"max"},{"Date":"2021-07-12T04:00:00Z","Close":19.06,"Type":"min"},{"Date":"2021-07-09T04:00:00Z","Close":17.78,"Type":"max"},{"Date":"2021-07-01T04:00:00Z","Close":25.07,"Type":"min"}]
        if FilterSupplyDemandZone.db is None:
            FilterSupplyDemandZone.db = DB()
        if len(FilterSupplyDemandZone.keylevels) <= 0:
            levels = self.readAllFromDb()
            for row in levels:
                try:
                    symbol = row[0]
                    data = row[1]
                    FilterSupplyDemandZone.keylevels[symbol] = data
                except Exception as ex:
                    logging.error(f'FilterSupplyDemandZone.__init__ {row}')


    def readAllFromDb(self):
        query = """SELECT symbol, keylevels FROM public.market_data WHERE timeframe=%s AND NOT is_deleted ORDER BY symbol asc"""
        params = ('1Day',)
        isOk, results = self.db.SelectQuery(query, params)
        if isOk:
            return results
        return None

    def readFromDb(self, symbol):
        levels = filter(lambda row: row.symbol == symbol, FilterSupplyDemandZone.keylevels)
        return levels

    def cleanLevels(self, df:pd.DateOffset) -> list:
        newlevels = []
        for row1 in range(len(df)):
            lastvalue = 0
            usedOnce = False
            keyvalue = df.iloc[row1]['Close']
            for row2 in range(row1+1, len(df)):
                newvalue = df.iloc[row2]['Close']
                if lastvalue != 0:
                    if (lastvalue >= keyvalue >= newvalue) or (lastvalue <= keyvalue <= newvalue):
                        usedOnce = True
                lastvalue = newvalue
            if not usedOnce:
                newlevels.append(df.iloc[row1]['Close'])
        return newlevels

    def isPriceNearSD(self, close:float, values:list, range:float = None):
        range = 0.05 if range is None else range
        for value in values:
            price = value
            low = price * (1 - range)
            high = price * (1 + range)
            if high > close > low:
                return True
        return False

    def Run(self, symbol:str, close: float):
        try:
            datalist = self.keylevels[symbol]
            df:pd.DataFrame = pd.DataFrame(datalist)
            newValues:list = self.cleanLevels(df[::-1])
            isSDZ = self.isPriceNearSD(close, newValues)
            return isSDZ
        except Exception as ex:
            logging.error(f'FilterSupplyDemandZone {symbol} - {ex}')
            return False

if __name__ == '__main__':
    one = FilterSupplyDemandZone()
    result = one.Run('FNV', 164.40)
    print(result)

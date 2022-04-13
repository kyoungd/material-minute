import numpy as np
import pandas as pd
import os
import copy
from scipy.signal import argrelextrema
import logging
from dbase import MarketDataDb
from .allstocks import AllStocks
from .environ import EnvFile
from datetime import datetime


class TightMinMax:
    db = None

    def __init__(self, isSaveToDb=None, tightMinMaxN=None, colName=None):
        self.colName = 'Close' if colName is None else colName
        n = int(EnvFile.Get('TIGHT_MINMAX_N', '2'))
        self.minMaxN = n if tightMinMaxN is None else tightMinMaxN
        self.isSaveToDb = False if isSaveToDb is None else isSaveToDb
        if TightMinMax.db is None:
            TightMinMax.db = MarketDataDb()

    def getRangeMax(self, df):
        rows = []
        for _, row in df.iterrows():
            open = row[1]['Open']
            close = row[1]['Close']
            rows.append(open if open > close else close)
        return rows

    def getRangeMin(self, df):
        rows = []
        for _, row in df.iterrows():
            open = row[1]['Open']
            close = row[1]['Close']
            rows.append(open if open < close else close)
        return rows

    def minMaxItem(self, onedate, close, onetype):
        return {'Date': onedate, 'Close': close, 'Type': onetype}

    def removeDuplicateMinMax(self, df):
        firstMin = False
        l_minmax = None
        minMaxSet = []
        for ix in range(len(df.index)):
            ldate = df.iloc[ix]['Date']
            lmin = df.iloc[ix]['min']
            lmax = df.iloc[ix]['max']
            if not np.isnan(lmin):
                value = lmin
                if l_minmax is None:
                    l_minmax = self.minMaxItem(ldate, value, 'min')
                    minMaxSet.append(l_minmax)
                    firstMin = True
                else:
                    newType = 'max'
                    if l_minmax['Type'] != newType:
                        l_minmax = self.minMaxItem(ldate, value, newType)
                        minMaxSet.append(l_minmax)
                    else:
                        if value < l_minmax['Close']:
                            minMaxSet.pop()
                            l_minmax = self.minMaxItem(ldate, value, newType)
                            minMaxSet.append(l_minmax)
            elif not np.isnan(lmax):
                value = lmax
                if l_minmax is None:
                    l_minmax = self.minMaxItem(ldate, value, 'max')
                    minMaxSet.append(l_minmax)
                    firstMin = False
                else:
                    newType = 'min'
                    if l_minmax['Type'] != newType:
                        l_minmax = self.minMaxItem(ldate, value, newType)
                        minMaxSet.append(l_minmax)
                    else:
                        if value > l_minmax['Close']:
                            minMaxSet.pop()
                            l_minmax = self.minMaxItem(ldate, value, newType)
                            minMaxSet.append(l_minmax)
        df1 = pd.DataFrame(minMaxSet)
        return firstMin, df1

    def getMinMax(self, df):
        df = df.reset_index()
        n = self.minMaxN        # number of points to be checked before and after

        df['up'] = self.getRangeMax(df)
        df['down'] = self.getRangeMin(df)

        df['min'] = df.iloc[argrelextrema(df['down'].values, np.less_equal,
                            order=n)[0]]['down']
        df['max'] = df.iloc[argrelextrema(df['up'].values, np.greater_equal,
                            order=n)[0]]['up']

        isFirstMin, df1 = self.removeDuplicateMinMax(df)
        return isFirstMin, df1

    def readFromDb(self, symbol):
        query = """SELECT keylevels, is_first_key_level_min FROM public.market_data WHERE symbol=%s AND timeframe=%s AND NOT is_deleted"""
        params = (symbol, '1Day')
        isOk, results = TightMinMax.db.SelectQuery(query, params)
        if isOk:
            row = results[0]
            data = row[0]
            isFirstKeyLevelMin = row[1]
            return isFirstKeyLevelMin, data
        return False, None

    def saveToDb(self, symbol, isFirstMin, data):
        time_now = datetime.now()
        query = """UPDATE public.market_data SET keylevels=%s, is_first_key_level_min=%s, updated_at=%s WHERE symbol=%s AND timeframe=%s AND NOT is_deleted"""
        params = (data, isFirstMin, time_now, symbol, '1Day')
        TightMinMax.db.UpdateQuery(query, params)

    def Run(self, symbol):
        try:
            if not self.isSaveToDb:
                isFirstMin, df = self.readFromDb(symbol)
                if df is not None:
                    return isFirstMin, pd.DataFrame(df)
            isOk, df = AllStocks.GetDailyStockData(symbol)
            if isOk:
                isFirstMin, df1 = self.getMinMax(df)
                if self.isSaveToDb:
                    data = df1.to_json(orient='records')
                    self.saveToDb(symbol, isFirstMin, data)
                return isFirstMin, df1
            return False, None
        except Exception as e:
            logging.error(f'TightMinMax.Run: {symbol} - {e}')
            print(f'TightMinMax.Run: {symbol} - {e}')

    @staticmethod
    def All():
        app = TightMinMax(isSaveToDb=True)
        AllStocks.Run(app.Run, False)


if __name__ == '__main__':
    symbol = 'AAPL'
    isLoaded, df = AllStocks.GetDailyStockData(symbol)
    if isLoaded:
        app = TightMinMax(df)
        firstMin, df = app.Run()
        print(df)
        print(firstMin)
    print('done')

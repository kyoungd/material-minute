import numpy as np
import pandas as pd
import os
import copy
from scipy.signal import argrelextrema
import logging
from environ import EnvFile
from datetime import datetime


class TightMinMax:
    def __init__(self, tightMinMaxN=None, colName=None):
        self.colName = 'Close' if colName is None else colName
        n = int(EnvFile.Get('TIGHT_MINMAX_N', '2'))
        self.minMaxN = n if tightMinMaxN is None else tightMinMaxN

    def getRangeMax(self, df):
        rows = []
        for _, row in df.iterrows():
            data = max(row['Open'], row['Close'])
            rows.append(data)
        return rows

    def getRangeMin(self, df):
        rows = []
        for _, row in df.iterrows():
            data = min(row['Open'], row['Close'])
            rows.append(data)
        return rows

    def minMaxItem(self, idx:int, onedate:str, close:float, onetype:str):
        return {'x': idx, 'Date': onedate, 'Close': close, 'Type': onetype}

    def isDuplicate(self, lastMinMax:float, currMinMax:float) -> bool:
        data = lastMinMax / currMinMax
        if 1.01 >= data >= 0.99:
            return True
        return False

    def removeDuplicateMinMax(self, df):
        firstMin = False
        l_minmax = None
        minMaxSet = []
        for ix in df.index:
            if ix > 0:
                ldate = df.iloc[ix]['Date']
                lmin = df.iloc[ix]['min']
                lmax = df.iloc[ix]['max']
                if not np.isnan(lmin):
                    value = lmin
                    newType = 'min'
                elif not np.isnan(lmax):
                    value = lmax
                    newType = 'max'
                else:
                    value = None
                if value is not None:
                    if l_minmax is None:
                        l_minmax = self.minMaxItem(ix, ldate, value, newType)
                        minMaxSet.append(l_minmax)
                    elif not self.isDuplicate(l_minmax['Close'], value):
                        if l_minmax['Type'] != newType:
                            l_minmax = self.minMaxItem(ix, ldate, value, newType)
                            minMaxSet.append(l_minmax)
                        else:
                            if (newType == 'min' and value < l_minmax['Close']) or (newType == 'max' and value > l_minmax['Close']):
                                if len(minMaxSet) == 1:
                                    minMaxSet[0]['Type'] = 'max' if newType == 'min' else 'min'
                                else:
                                    minMaxSet.pop()
                                l_minmax = self.minMaxItem(ix, ldate, value, newType)
                                minMaxSet.append(l_minmax)
        firstMin = True if len(minMaxSet) > 0 and minMaxSet[0]['Type'] == 'min' else False
        df1 = pd.DataFrame(minMaxSet)
        return firstMin, df1

    def removeRepeatMinMax(self, df):
        firstMin = False
        l_minmax = None
        minMaxSet = []
        lastMinMax = ''
        for ix in df.index:
            if ix > 0 and ix < len(df)-1:
                ldate = df.iloc[ix]['Date']
                lmin = df.iloc[ix]['min']
                lmax = df.iloc[ix]['max']
                if not np.isnan(lmin):
                    if lastMinMax != 'min':
                        l_minmax = self.minMaxItem(ix, ldate, lmin, 'min')
                        lastMinMax = 'min'
                        minMaxSet.append(l_minmax)
                elif not np.isnan(lmax):
                    if lastMinMax != 'max':
                        l_minmax = self.minMaxItem(ix, ldate, lmax, 'max')
                        lastMinMax = 'max'
                        minMaxSet.append(l_minmax)
        df1 = pd.DataFrame(minMaxSet)
        return firstMin, df1

    def Run(self, df:pd.DataFrame, isRemoveRepeatMinMaxOnly=None):
        isRemoveRepeatMinMaxOnly = False if isRemoveRepeatMinMaxOnly is None else isRemoveRepeatMinMaxOnly
        df = df.reset_index()
        n = self.minMaxN        # number of points to be checked before and after

        df['up'] = self.getRangeMax(df)
        df['down'] = self.getRangeMin(df)

        df['min'] = df.iloc[argrelextrema(df['down'].values, np.less_equal,
                            order=n)[0]]['down']
        df['max'] = df.iloc[argrelextrema(df['up'].values, np.greater_equal,
                            order=n)[0]]['up']

        if isRemoveRepeatMinMaxOnly:
            isFirstMin, df1 = self.removeRepeatMinMax(df)
            return isFirstMin, df1
        else:
            isFirstMin, df1 = self.removeDuplicateMinMax(df)
            return isFirstMin, df1

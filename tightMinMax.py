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

    def Run(self, df:pd.DataFrame):
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

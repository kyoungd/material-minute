import numpy as np
import pandas as pd
from scipy.signal import argrelextrema
from environ import EnvFile
import os


class LocalMinMax:
    def __init__(self, colName=None, degreeFit=None):
        self.colName = 'Close' if colName is None else colName
        self.degreeFit = int(EnvFile.Get('LOCAL_MINMAX_N', '30')) if degreeFit is None else degreeFit

    def Polyfit(self, df: pd.DataFrame, colName:str, degreeFit:int):
        # discrete dataset
        x_data = df.index.tolist()      # the index will be our x axis, not date
        y_data = df[colName]
        t_data = df['Date']

        # x values for the polynomial fit, 200 points
        x = np.linspace(0, max(df.index.tolist()),
                        max(df.index.tolist()) + 1)

        # polynomial fit of degree xx
        pol = np.polyfit(x_data, y_data, degreeFit)
        y_pol = np.polyval(pol, x)

        data = y_pol

        # ___ detection of local minimums and maximums ___

        min_max = np.diff(np.sign(np.diff(data))).nonzero()[
            0] + 1          # local min & max
        l_min = (np.diff(np.sign(np.diff(data))) >
                 0).nonzero()[0] + 1      # local min
        l_max = (np.diff(np.sign(np.diff(data))) <
                 0).nonzero()[0] + 1      # local max

        # ___ package local minimums and maximums for return  ___

        # dfMin = None if len(l_min) < 0 else pd.DataFrame.from_dict(
        #     {'Date': t_data[l_min].values, colName: data[l_min]})
        # dfMax = pd.DataFrame.from_dict(
        #     {'Date': t_data[l_max].values, colName: data[l_max]})
        # return dfMin, dfMax

        l_minmax = np.sort(np.append(l_min, l_max))
        isFirstMinimum = True if l_min[len(
            l_min)-1] < l_max[len(l_max)-1] else False
        timeframes = t_data[l_minmax].values
        closes = data[l_minmax]
        df = pd.DataFrame.from_dict({'Date': timeframes, colName: closes})
        return isFirstMinimum, df

    def minMaxItem(self, onedate, close, onetype):
        return {'Date': onedate, f'{self.colName}': close, 'Type': onetype}

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
                        if value < l_minmax[self.colName]:
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
                        if value > l_minmax[self.colName]:
                            minMaxSet.pop()
                            l_minmax = self.minMaxItem(ldate, value, newType)
                            minMaxSet.append(l_minmax)
        df1 = pd.DataFrame(minMaxSet)
        return firstMin, df1

    def Run(self, dataf: pd.DataFrame):
        df = dataf.reset_index()
        firstMin, df = self.Polyfit(df, self.colName, self.degreeFit)
        isFirstMin, df1 = self.removeDuplicateMinMax(df)
        return isFirstMin, df1


if __name__ == '__main__':
    pass

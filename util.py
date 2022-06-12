import numpy as np
import matplotlib.pyplot as plt
import requests
import pandas as pd
import talib

class Util:
    minMaxRangePercent = 0.06
    minMaxNearPercent = 0.04
    minMaxPricePercentSlope = 1

    @staticmethod
    def slope(x1: float, y1: float, x2: float, y2: float, x: float) -> float:
        if x1 - x2 == 0:
            return y1
        m = (y2 - y1) / (x2 - x1)
        v = m * (x-x1) + y1
        return v

    @staticmethod
    def SlopeOfPrice(close: float, slope: float = None) -> float:
        data1: float = Util.slope(
            3, Util.minMaxPricePercentSlope, 200, Util.minMaxPricePercentSlope/3, close)
        return data1

    @staticmethod
    def IsSameSign(number1: float, number2: float):
        if number1 > 0 and number2 > 0:
            return True
        if number1 < 0 and number2 < 0:
            return True
        return False

    @staticmethod
    def DistanceSlope(distance: int) -> float:
        return Util.slope(3, 1, 20, 0.3, distance)

    @staticmethod
    def StandardPrice(price: float) -> float:
        return price * Util.slope(3, 3, 300, 0.3, price)

    @staticmethod
    def StandarizePriceDf(df: pd.DataFrame) -> pd.DataFrame:
        df['Close'] = df['Close'].apply(Util.StandardPrice)
        df['Open'] = df['Open'].apply(Util.StandardPrice)
        df['High'] = df['High'].apply(Util.StandardPrice)
        df['Low'] = df['Low'].apply(Util.StandardPrice)
        return df

    @staticmethod
    def IsEnoughSpread(df: pd.DataFrame, spread:float = None):
        spread = Util.minMaxRangePercent if spread is None else spread
        iMax = df['High'].idxmax()
        iMin = df['Low'].idxmin()
        high = df.iloc[iMax]['High']
        low = df.iloc[iMin]['Low']
        return Util.IsPriceSpread(high, low, spread)

    @staticmethod
    def IsPriceSpread(price1: float, price2: float, spread: float = None) -> bool:
        spread = Util.minMaxRangePercent if spread is None else spread
        spreadPrice = spread * (price1 + price2) / 2.0
        if abs(price1 - price2) >= spreadPrice:
            return True
        return False

    @staticmethod
    def IsNearPrice(close1: float, close2: float, spread:float = None) -> bool:
        spread = Util.minMaxNearPercent if spread is None else spread
        priceDelta = spread * (close1 + close2) / 2
        if abs(close2 - close1) <= abs(priceDelta):
            return True
        return False

    @staticmethod
    def GetHighestLowestDf(df: pd.DataFrame, columnNameHigh:str, columneNameLow:str) -> set:
        iMax = df[columnNameHigh].idxmax()
        iMin = df[columneNameLow].idxmin()
        high = df.iloc[iMax][columnNameHigh]
        low = df.iloc[iMin][columneNameLow]
        return high, low

    @staticmethod
    def GetHighestLowestIndexDf(df: pd.DataFrame, columnNameHigh:str, columneNameLow:str) -> set:
        iMax = df[columnNameHigh].idxmax()
        iMin = df[columneNameLow].idxmin()
        return iMax, iMin


    # IF CHOPPINESS INDEX >= 61.8 - -> MARKET IS CONSOLIDATING
    # IF CHOPPINESS INDEX <= 38.2 - -> MARKET IS TRENDING
    # https://medium.com/codex/detecting-ranging-and-trending-markets-with-choppiness-index-in-python-1942e6450b58
    @staticmethod
    def ChoppinessIndex(high, low, close, lookback=None):
        lookback = 14 if lookback is None else lookback
        tr1 = pd.DataFrame(high - low).rename(columns={0: 'tr1'})
        tr2 = pd.DataFrame(abs(high - close.shift(1))).rename(columns={0: 'tr2'})
        tr3 = pd.DataFrame(abs(low - close.shift(1))).rename(columns={0: 'tr3'})
        frames = [tr1, tr2, tr3]
        tr = pd.concat(frames, axis=1, join='inner').dropna().max(axis=1)
        atr = tr.rolling(1).mean()
        highh = high.rolling(lookback).max()
        lowl = low.rolling(lookback).min()
        ci = 100 * np.log10((atr.rolling(lookback).sum()) /
                            (highh - lowl)) / np.log10(lookback)
        return ci

    # tsla['ci_14'] = ChoppinessIndex(tsla['high'], tsla['low'], tsla['close'], 14)
    # tsla = tsla.dropna()

    @staticmethod
    def IsTrending(choppinessValue: float) -> bool:
        if choppinessValue <= 38.2:
            return True
        return False

    @staticmethod
    def IsConsolidating(chopinessValue: float) -> bool:
        if chopinessValue >= 61.8:
            return True
        return False
    
    @staticmethod
    def GetEma(df: pd.DataFrame, emaName:str = None, lookback: int = None) -> pd.DataFrame:
        colName = 'ema9' if emaName is None else emaName
        lookback = 9 if lookback is None else lookback
        df1 = df[::-1]
        df1 = df1.reset_index()
        closesMean = talib.EMA(df1.Close, lookback)
        df1[colName] = closesMean
        # df2 = df1.assign(ema9=closesMean)
        df1 = df1[::-1]
        df1 = df1.reset_index()
        return df1

    @staticmethod
    def IsAboveEma(df: pd.DataFrame, indexA: int, indexB: int, emaName) -> bool:
        colName = 'ema9' if emaName is None else emaName
        isMovingUp = True if df.iloc[indexA].Close < df.iloc[indexB].Close else False
        for idx in range(indexA, indexB):
            close = df.iloc[idx].Close
            emaN = df.iloc[idx][colName]
            if isMovingUp and close < emaN:
                return False
            if not isMovingUp and close > emaN:
                return False
        return True

    @staticmethod
    def IsAboveOtherEma(df: pd.DataFrame, indexA: int, indexB: int, emaColNameA:str, emaColNameB:str) -> bool:
        isMovingUp = True if df.iloc[indexA].Close < df.iloc[indexB].Close else False
        for idx in range(indexA, indexB):
            emaA = df.iloc[idx][emaColNameA]
            emaB = df.iloc[idx][emaColNameB]
            if isMovingUp and emaA < emaB:
                return False
            if not isMovingUp and emaA > emaB:
                return False
        return True


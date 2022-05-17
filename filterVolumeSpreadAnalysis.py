import pandas as pd
import os

class volumeSpreadAnalysis:
    def __init__(self):
        self.barCount: int = 4
        self.averagingBarCount: int = 4
        self.factor3 = 1.8
        self.factor4 = 1.8
        self.factor5 = 1.8
        self.factor8 = 1.8
        self.factor11 = 3.0

    def isCanCalculate(self, df: pd.DataFrame, period: int):
        return False if len(df) < period else True

    def avgSwing(self, df: pd.DataFrame, swingFunc) -> float:
        swingTotal: float = 0
        swingPeriod: int = self.averagingBarCount if len(
            df) > self.averagingBarCount else len(df)
        swingMax: float = 0
        for _, row in df[:swingPeriod].iterrows():
            swing = swingFunc(row)
            swingMax = max(swingMax, swing)
            swingTotal += swing
        oneAvgSwing: float = (swingTotal - swingMax) / (swingPeriod - 1)
        return oneAvgSwing

    def avgHighLowSwing(self, df: pd.DataFrame) -> float:
        return self.avgSwing(df, lambda row: abs(row.High - row.Low))

    def avgVolumeSwing(self, df: pd.DataFrame) -> float:
        return self.avgSwing(df, lambda row: abs(row.Volume))

    def avgOpenCloseSwing(self, df: pd.DataFrame) -> float:
        return self.avgSwing(df, lambda row: abs(row.Close - row.Open))

    def getVariables(self, df: pd.DataFrame, avgSpread: float, avgVolume: float):
        spreads = []
        volumes = []
        for _, row in df[0:5].iterrows():
            spread = (row.Close - row.Open) / avgSpread
            volume = row.Volume / avgVolume
            spreads.append(spread)
            volumes.append(volume)
        return spreads, volumes

    def isPositive(self, number: float):
        if number < 0:
            return False
        return True

    def isSameSign(self, number1: float, number2: float):
        if number1 > 0 and number2 > 0:
            return True
        if number1 < 0 and number2 < 0:
            return True
        return False

    def isAboutSameSize(self, number1: float, number2: float):
        newPercent = abs(number2) / number1 if number1 != 0 else 0
        if newPercent > 0.8 and newPercent <= 1.2:
            return True
        return False

    def wyckoffDoji(self, df: pd.DataFrame, spreads: list, volumes: list, period: int) -> int:
        ix = 0
        s1 = spreads[ix]
        s2 = spreads[ix+1]
        s3 = spreads[ix+2]
        if abs(s1) > 0.1:
            return 0
        if abs(s1) > abs(s2) or abs(s2) > abs(s3):
            return 0
        v1 = volumes[ix]
        v2 = volumes[ix+1]
        v3 = volumes[ix+2]
        if abs(v1) > abs(v2) or abs(v1) > abs(v3):
            return 0
        c1 = df.iloc[ix].Close
        c2 = df.iloc[ix+1].Close
        c3 = df.iloc[ix+2].Close
        o1 = df.iloc[ix].Open
        o2 = df.iloc[ix+1].Open
        o3 = df.iloc[ix+2].Open
        if c1 >= c2 and c2 > c3 and c2 > o2 and c3 > o3:
            h1 = df.iloc[ix].High
            h2 = df.iloc[ix+1].High
            h3 = df.iloc[ix+2].High
            if h1 >= h2:
                return 10
        if c1 <= c2 and c2 < c3 and c2 < o2 and o3 < c3:
            l1 = df.iloc[ix].Low
            l2 = df.iloc[ix+1].Low
            l3 = df.iloc[ix+2].Low
            if l1 <= l2:
                return 10
        return 0

    def localMinMax(self, df: pd.DataFrame, index: int, barCount=None):
        iMax = df['Close'].idxmax()
        iMin = df['Close'].idxmin()
        if iMax == index or iMin == index:
            return True
        return False


    def isVsaOk(self, df: pd.DataFrame, spreads: list, volumes: list, period: int) -> int:
        ix = 0
        s1 = spreads[ix]
        s2 = spreads[ix+1]
        s3 = spreads[ix+2]
        s4 = spreads[ix+3]
        v1 = volumes[ix]
        v2 = volumes[ix+1]
        v3 = volumes[ix+2]
        v4 = volumes[ix+3]
        # down thrust
        if abs(s2) < 0.3 and v2 > 2.5 and not self.isSameSign(s1, s2) and self.isSameSignal(s2, s3) and self.isSameSignal(s2, s4):
            if self.localMinMax(df, 1, 4):
                return 1
        # selling climax
        if abs(s2) > 3 and v2 > 2.5 and not self.isSameSign(s1, s2) and abs(s2) > abs(s1) and self.isSameSign(s2, s3) and self.isSameSign(s2, s4):
            if self.localMinMax(df, 1, 4):
                return 2

        #
        # if not self.isSameSign(s2, s4) and self.isSameSign(s1, s2):
        #     if abs(s2) > abs(s3) * self.factor11 and abs(s4) > abs(s3) * self.factor11:
        #         return 11
        #

        return 0

    def Run(self, symbol: str, df: pd.DataFrame) -> int:
        period = self.averagingBarCount
        if self.isCanCalculate(df, period):
            avgV = self.avgVolumeSwing(df)
            avgS = self.avgOpenCloseSwing(df)
            spreads, volumes = self.getVariables(df, avgS, avgV)
            vsa = self.wyckoffDoji(df, spreads, volumes, self.barCount)
            vsa = vsa if vsa > 0 else self.isVsaOk(
                df, spreads, volumes, self.barCount)
            return vsa
        else:
            return 0

    

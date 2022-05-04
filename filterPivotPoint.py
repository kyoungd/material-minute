from email.errors import FirstHeaderLineIsContinuationDefect
import pandas as pd
import os
from db import DB
import logging
from redisUtil import TimeStamp
from filterPriceSpread import FilterPriceSpread
from redisHash import PivotPointStack
from tightMinMax import TightMinMax
from util import Util


testdata = [{"t": "2022-04-14T13:19:00Z", "o": 7.12, "h": 7.12, "l": 7.12, "c": 7.12, "v": 200, "n": 2, "vw": 7.12}, 
            {"t": "2022-04-14T13:15:00Z", "o": 7.13, "h": 7.13, "l": 7.13, "c": 7.13, "v": 200, "n": 2, "vw": 7.13}, 
            {"t": "2022-04-14T13:09:00Z", "o": 7.14, "h": 7.14, "l": 7.14, "c": 7.14, "v": 100, "n": 1, "vw": 7.14}, 
            {"t": "2022-04-14T13:08:00Z", "o": 7.14, "h": 7.14, "l": 7.14, "c": 7.14, "v": 400, "n": 2, "vw": 7.14}, 
            {"t": "2022-04-14T13:07:00Z", "o": 7.16, "h": 7.16, "l": 7.16, "c": 7.16, "v": 214, "n": 3, "vw": 7.16}]

class LoadPivotPoints:
    def __init__(self):
        self.hash = PivotPointStack()

    def AddPivotPoint(self, block):
        try:
            symbol = block[0]
            latest = block[1][0]
            pp = (latest['h'] + latest['l'] + latest['c']) / 3
            r1 = 2 * pp - latest['l']
            s1 = 2 * pp - latest['h']
            data = { "pp": pp, "r1": r1, "s1": s1 }
            self.hash.Add(symbol, data)
        except Exception as ex:
            logging.error(f'LoadPivotPoints.AddPivotPoint {symbol} - {ex}')


    def readFromDb(self, func):
        db = DB()
        query = """SELECT symbol, data FROM public.market_data WHERE timeframe='1Day' AND NOT is_deleted"""
        isOk, results = db.SelectQuery(query, ())
        if isOk:
            lineCount = 0
            for symbol in results:
                lineCount += 1
                if (lineCount % 100) == 0:
                    print(lineCount)
                func(symbol)

    def Run(self):
        self.hash.Reset()
        self.readFromDb(self.AddPivotPoint)


class FilterPivotPoint:

    def __init__(self, marketOpenAt=None):
        self.takeoffSlope = 0.10
        self.minMaxNearPercent = 0.03
        self.hash = PivotPointStack()
        self.fMinmax = TightMinMax(tightMinMaxN=5)

    def IsItReady(self, pivot: dict, dataf: pd.DataFrame, close: float) -> bool:
        if not FilterPriceSpread.IsNearPrice(close, pivot['pp'], 0.03):
            return False
        return True

    def beforeAndAfterSlope(self, df: pd.DataFrame, close: float) -> pd.DataFrame:
        lastRow = None
        takeOffSlopes = []
        for idx, row in df.iterrows():
            if not lastRow is None:
                slope = (row['Close'] - lastRow['Close']) / \
                    (row['x'] - lastRow['x'])
                standardSlope = slope * Util.SlopeOfPrice(close)
                takeOffSlopes.append(abs(standardSlope))
            lastRow = row
        if len(df) > 0:
            takeOffSlopes.append(0)
        df = df.assign(Takeoff=takeOffSlopes)
        return df

    def IsPivotPointCenter(self, pivot: dict, dataf: pd.DataFrame, close: float) -> bool:
        close = dataf.iloc[0]['Close']
        if self.IsItReady(pivot, dataf, close):
            isPtMin, keypoints = self.fMinmax.Run(dataf)
            keypoints: pd.DataFrame = self.beforeAndAfterSlope(
                keypoints, close)
            firstMinMax = keypoints.iloc[0]
            if FilterPriceSpread.IsNearPrice(pivot['pp'], firstMinMax['Close'], self.minMaxNearPercent):
                distance = 1
                if len(keypoints) > 1:
                    distance = abs(keypoints.iloc[1].x - keypoints.iloc[0].x)
                takeoff = firstMinMax['Takeoff'] / Util.DistanceSlope(distance)
                if takeoff > self.takeoffSlope:
                    return True
                else: # kyd
                    logging.info(f'filterPivotPoint: ${close:.2f} {takeoff:.2f}% ')
        return False
    
    def Run(self, symbol: str, dataf: pd.DataFrame, close: float, isDebug:bool = None) -> bool:
        try:
            close = dataf.iloc[0]['Close']
            # less than 15 minutes into the market.  too early.
            if len(dataf) < 3:
                return False
            pivot = self.hash.Get(symbol)
            if pivot is None:
                return False
            if self.IsItReady(pivot, dataf, close):
                return self.IsPivotPointCenter(pivot, dataf, close)
        except Exception as ex:
            logging.error(f'FilterDailySupplyDemandZone {symbol} - {ex}')
            return False

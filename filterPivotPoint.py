from email.errors import FirstHeaderLineIsContinuationDefect
import pandas as pd
import os
from db import DB
import logging
from redisUtil import TimeStamp
from filterPriceSpread import FilterPriceSpread
from redisHash import PivotPointStack
from tightMinMax import TightMinMax


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
        self.marketOpenAt = TimeStamp.getMarketOpenTimestamp(
        ) if marketOpenAt is None else marketOpenAt
        self.minMaxRangePercent = 0.06
        self.minMaxNearPercent = 0.04
        self.hash = PivotPointStack()
        self.fMinmax = TightMinMax(tightMinMaxN=5)

    def IsItReady(self, pivot:dict, dataf: pd.DataFrame, close: float) -> bool:
        highest = dataf['High'].loc[dataf['High'].idxmax()]
        # Minimum in column
        lowest = dataf['Low'].loc[dataf['Low'].idxmin()]
        # if the stock crosses the pivot, return false
        if highest >= pivot['pp'] >= lowest:
            return False
        # if spread is not enough
        if not FilterPriceSpread.IsPriceSpread(highest, pivot['pp'], 0.04) and not FilterPriceSpread.IsPriceSpread(lowest, pivot['pp'], 0.04):
            return False
        # if first point:
        openingClose = dataf.iloc[-1]['Close']
        if not FilterPriceSpread.IsNearPrice(openingClose, pivot['pp'], 0.03):
            return False
        if FilterPriceSpread.IsNearPrice(close, pivot['pp'], 0.03):
            return False
        # isOk, peaks = self.fMinmax.Run(dataf[::-1])
        # if len(peaks) % 2 == 0:
        #     return False
        return True

    def IsPivotPointInPlay(self, pivot: dict, dataf: pd.DataFrame, close: float) -> bool:
        _, keypoints = self.fMinmax.Run(dataf[::-1], isRemoveRepeatMinMaxOnly=True)
        if len(keypoints) > 0 and len(keypoints) % 2 == 1:
            return True
        return False
    
    def Run(self, symbol: str, dataf: pd.DataFrame, close: float) -> bool:
        try:
            dataf = dataf[dataf['Date'] >= self.marketOpenAt]
            # less than 15 minutes into the market.  too early.
            if len(dataf) < 3:
                return False
            pivot = self.hash.Get(symbol)
            if pivot is None:
                return False
            if self.IsItReady(pivot, dataf, close):
                return self.IsPivotPointInPlay(pivot, dataf, close)
            return False
        except Exception as ex:
            logging.error(f'FilterDailySupplyDemandZone {symbol} - {ex}')
            return False
#

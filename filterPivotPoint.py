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
        symbol = block["symbol"]
        rows = block["data"]
        pp = (rows[0]['h'] + rows[0]['l'] + rows[0]['c']) / 3
        r1 = 2 * pp - rows[0]['l']
        s1 = 2 * pp - rows[0]['h']
        data = { "pp": pp, "r1": r1, "s1": s1 }
        self.hash.Add(symbol, data)

    def readFromDb(self, func)
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
        self.fMinmax = TightMinMax(tightMinMaxN=4)

    def Run(self, symbol: str, dataf: pd.DataFrame, close: float) -> bool:
        try:
            dataf = dataf[dataf['DateTime'] > self.marketOpenAt]
            # less than 15 minutes into the market.  too early.
            if len(dataf) < 3:
                return False
            pivot = self.hash.Get(symbol)
            highest = dataf['High'].loc[dataf['High'].idxmax()]
            lowest = dataf['Low'].loc[dataf['Low'].idxmin()]      # Minimum in column
            # if the stock crosses the pivot.  It already crossed.
            if highest > pivot['pp'] > lowest:
                return False
            # if spread is not enough
            if FilterPriceSpread.IsEnoughSpread(highest, lowest, )

            firstPt = dataf.iloc[len(dataf) - 1]
            
            bars = dataf[::-1]

            firstPt = bars[0]
            lastPt = bars[len(bars)-1]
            if FilterPriceSpread.IsNearPrice(lastPt[0]['Low'], pivot['pp'], self.getPivotPointSpread(pivot['pp'])):
            if FilterPriceSpread.IsNearPrice(firstPt[0]['High'], pivot['pp'], self.getPivotPointSpread(pivot['pp'])):
                pass
            elif FilterPriceSpread.IsNearPrice(firstPt[0]['Low'], pivot['pp'], self.getPivotPointSpread(pivot['pp'])):
                pass
            else
                return False
            df = self.fMinmax.Run(dataf)
            if len(df) <= 1:
                return False
            if len(df) == 1:
                pass
            if len(df) == 3:
                pass
            if len(df) == 5:
                pass
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

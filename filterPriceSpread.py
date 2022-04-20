import pandas as pd

class FilterPriceSpread:
    minMaxRangePercent = 0.06
    minMaxNearPercent = 0.04

    @staticmethod
    def slope(x1: float, y1: float, x2: float, y2: float, x: float) -> float:
        if x1 - x2 == 0:
            return y1
        m = (y2 - y1) / (x2 - x1)
        v = m * (x-x1) + y1
        return v

    @staticmethod
    def IsEnoughSpread(df: pd.DataFrame, spread:float = None):
        spread = FilterPriceSpread.minMaxRangePercent if spread is None else spread
        iMax = df['High'].idxmax()
        iMin = df['Low'].idxmin()
        high = df.iloc[iMax]['High']
        low = df.iloc[iMin]['Low']
        return FilterPriceSpread.IsPriceSpread(high, low, spread)

    @staticmethod
    def IsPriceSpread(price1: float, price2: float, spread: float = None) -> bool:
        spread = FilterPriceSpread.minMaxRangePercent if spread is None else spread
        adjSpread = FilterPriceSpread.slope(
            3, spread, 200, spread/3.0, (price1 + price2)/2.0)
        spreadPrice = adjSpread * (price1 + price2) / 2.0
        if abs(price1 - price2) >= spreadPrice:
            return True
        return False

    @staticmethod
    def IsNearPrice(close1: float, close2: float, spread:float = None) -> bool:
        spread = FilterPriceSpread.minMaxNearPercent if spread is None else spread
        adjSpread = FilterPriceSpread.slope(3, spread,
                            200, spread / 3, close2)
        priceDelta = adjSpread * (close1 + close2) / 2
        if abs(close2 - close1) <= abs(priceDelta):
            return True
        return False

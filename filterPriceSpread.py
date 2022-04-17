import pandas as pd

class FilterPriceSpread:
    minMaxRangePercent = 0.06
    minMaxNearPercent = 0.04

    @staticmethod
    def slope(x1: int, y1: float, x2: int, y2: float, x: int) -> float:
        if x < x1:
            return y1
        if x > x2:
            return y2
        m = (y2 - y1) / (x2 - x1)
        v = m * x + x1
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
        highRange = FilterPriceSpread.minMaxRangePercent if spread is None else spread
        lowRange = highRange / 3
        spreadPrice = FilterPriceSpread.slope(
            3, highRange, 200, lowRange, price1)
        if abs(price1 - price2) <= spreadPrice:
            return True
        return False

    @staticmethod
    def IsNearPrice(close1: float, close2: float, spread:float = None) -> bool:
        spread = FilterPriceSpread.minMaxNearPercent if spread is None else spread
        priceDelta = FilterPriceSpread.slope(3, spread,
                            200, spread / 3, close2)
        if abs(close2 - close1) <= abs(priceDelta):
            return True
        return False

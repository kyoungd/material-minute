import json
import pandas as pd

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

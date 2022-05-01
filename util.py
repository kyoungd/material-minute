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

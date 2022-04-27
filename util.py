
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

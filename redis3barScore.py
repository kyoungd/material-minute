from redisUtil import RedisTimeFrame
from redisTimeseriesData import RealTimeBars
from redisHash import StoreStack, StoreScore
from redisUtil import RedisTimeFrame

#
# This class perform three bar study on trade data.
#


class StudyThreeBarsScore:
    # stack: StoreStack: class to store and retrieve Stack data
    # rtb: RealTimeBars: class to retrieve real time data

    def __init__(self):
        self.stack = StoreStack()
        self.rtb = RealTimeBars()

    # two scoring.  This one tests for basic accpetable trade.
    def _isPriceRangeOptimal(self, newPrice, price1, price2):
        return (newPrice < price2 and newPrice >= price1)

    # two scoring.  This one tests for optimal trade pattern.
    def _isPriceRangeUsable(self, newPrice, price1, price2):
        priceChange = (price2 - price1) / 2
        if (newPrice < (price2 + priceChange) and newPrice > (price1 - priceChange)):
            return True
        return False

    #
    # score an individual stock pricing.
    # 4 point is given for optimal trade.
    # 2 point is given for acceptable trade.
    # 0 point is given for unacceptable trade.
    #
    def ThreeBarPlay(self, newPrice, realtime, stack):
        point = 0
        stackValue = stack['value']
        price1 = stackValue['firstPrice']
        price2 = stackValue['secondPrice']
        if (self._isPriceRangeOptimal(newPrice, price1, price2)):
            point = 4
        elif (self._isPriceRangeUsable(newPrice, price1, price2)):
            point = 2
        return point

    # get real time data.
    # get pricing data.
    # get stack data which includes the last two prices that meets three bar pattern
    # score the pricing data and save it into Score class.
    #
    def Process(self, package, getRealTimeData, getStackData):
        data = package
        symbol = data['symbol']
        study = StoreScore(symbol)
        newPrice = data['close']
        newVolume = data['volume']
        realtime = getRealTimeData(
            None, symbol, RedisTimeFrame.REALTIME)
        stack = getStackData(symbol)
        if (realtime != None and stack != None):
            study.score.Score = self.ThreeBarPlay(newPrice, realtime, stack)
            study.save()

    #
    # call the scoring method
    #
    def study(self, package, getRealTimeData=None, getStackData=None):
        if (getRealTimeData == None):
            getRealTimeData = self.rtb.RedisGetDataClose
        if (getStackData == None):
            getStackData = self.stack.value
        self.Process(package, getRealTimeData, getStackData)

    # print data for debugging
    def printAllScores(self, score):
        data = self.score.getAll()
        print(data)


def testGetStackData(symbol):
    return {'symbol': symbol, 'value': {
        'firstPrice': 13.50,
        'secondPrice': 14.00,
        'thirdPrice': 13.00,
        'timeframe': RedisTimeFrame.MIN2
    }}


def testGetRealTimeData(api, symbol, timeframe):
    return [
        (1603723600, 13.90),
        (1603722600, 13.87),
        (1603721600, 13.82),
        (1603720600, 13.79),
        (1603719600, 13.88),
        (1603718600, 13.80),
        (1603717600, 13.72),
        (1603716600, 13.69),
        (1603715600, 13.68),
        (1603714600, 13.65),
        (1603713600, 13.64),
        (1603712600, 13.65),
    ]


if __name__ == "__main__":
    package = {'close': 13.92,
               'high': 14.57,
               'low': 12.45,
               'open': 13.4584,
               'symbol': 'FANG',
               'timestamp': 1627493640000000000,
               'trade_count': 602,
               'volume': 213907,
               'vwap': 8.510506}
    app = StudyThreeBarsScore()
    app.study(package, getRealTimeData=testGetRealTimeData,
              getStackData=testGetStackData)


# STACK
#     return {'symbol': symbol, 'value': {
#         'firstPrice': 14.00,
#         'secondPrice': 15.00,
#         'thirdPrice': 14.52,
#     }}


# STOCK
# {'close': 8.565,
#  'high': 8.57,
#  'low': 8.45,
#  'open': 8.4584,
#  'symbol': 'BTBT',
#  'timestamp': 1627493640000000000,
#  'trade_count': 602,
#  'volume': 213907,
#  'vwap': 8.510506}


# def runThreeBarPlay():
#     StudyThreeBars.run(redisTimeseries, redisCore, realtimeBar)


# if __name__ == "__main__":
#     obj_now = datetime.now()
#     secWait = 61 - obj_now.second
#     time.sleep(secWait)
#     SetInterval(5, runThreeBarPlay)

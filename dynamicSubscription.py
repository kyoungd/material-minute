"""
In this example code we will show a pattern that allows a user to change
the websocket subscriptions as they please.
"""
import logging
import threading
import asyncio
import time
from alpaca_trade_api.stream import Stream
from alpaca_trade_api.common import URL
from redisUtil import AlpacaStreamAccess, KeyName
from redisPubsub import RedisSubscriber, RedisPublisher
from pubsubKeys import PUBSUB_KEYS


async def print_trade(t):
    try:
        data = {'symbol': t['S'],
                'close': t['p'], 'volume': t['s']}
        publisherTrade.publish(data)
        print('trade', data)
    except Exception as e:
        logging.warning(f'EVENT-TRADE.print_trade exception - {e}')


async def print_quote(q):
    print('quote', q)


async def print_bar(bar):
    try:
        seconds = bar['t'].seconds
        bar['t'] = seconds
        publisherBar.publish(bar)
        print('bar', bar)
    except Exception as e:
        logging.warning(f'EVENT-TRADE.print_bar exception - {e}')


PREVIOUS = None


def init():
    # conn.run()
    global subscriber
    subscriber = RedisSubscriber(
        PUBSUB_KEYS.EVENT_TRADE_SUBSCRIBE, None, callback=subscription)
    subscriber.start()
    global publisherTrade
    publisherTrade = RedisPublisher(PUBSUB_KEYS.EVENT_TRADE_NEW)
    global publisherBar
    publisherBar = RedisPublisher(PUBSUB_KEYS.EVENT_BAR_CANDIDATE)
    global isConnectionComplete
    isConnectionComplete = False


def consumer_thread():
    try:
        # make sure we have an event loop, if not create a new one
        loop = asyncio.get_event_loop()
        loop.set_debug(True)
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

    global conn
    conn = AlpacaStreamAccess.connection()

    conn.subscribe_bars(print_bar, '*')
    global PREVIOUS
    PREVIOUS = "AAPL"
    conn.run()


def subscription(data, isTestOnly: bool = False) -> None:
    try:
        if (conn == None):
            return
        # make sure we have an event loop, if not create a new one
        loop = asyncio.get_event_loop()
        loop.set_debug(True)
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())
    except Exception as e:
        logging.error(f'EVENT-TRADE.subscribeToTrade exception - {e}')
        return

    try:
        logging.info(f'EVENT-TRADE.subscription started')
        symbol = data['symbol']
        op = data['operation']
        if (op == 'SUBSCRIBE'):
            logging.info(f'subscribe to: {symbol}')
            if not isTestOnly:
                conn.subscribe_trades(print_trade, symbol)
        else:
            logging.info('unsubscribe to: {symbol}')
            if not isTestOnly:
                conn.unsubscribe_trades(symbol)
    except Exception as e:
        logging.warning(f'EVENT-TRADE.subscription exception - {e}')

#


def run():
    init()
    threading.Thread(target=consumer_thread).start()

    loop = asyncio.get_event_loop()

    time.sleep(5)  # give the initial connection time to be established
    isConnectionComplete = True


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                        level=logging.INFO)
    run()

    # subscription({'symbol': 'AAPL', 'operation': 'SUBSCRIBE'})
    # time.sleep(5)
    # subscription({'symbol': 'FB', 'operation': 'SUBSCRIBE'})
    # time.sleep(5)
    # subscription({'symbol': 'TLSA', 'operation': 'SUBSCRIBE'})
    # time.sleep(5)
    # subscription({'symbol': 'AAPL', 'operation': 'UNSUBSCRIBE'})
    # time.sleep(5)
    # subscription({'symbol': 'FB', 'operation': 'UNSUBSCRIBE'})
    # time.sleep(5)
    # subscription({'symbol': 'TLSA', 'operation': 'UNSUBSCRIBE'})
    # time.sleep(5)

    # subscriptions = {"BABA": print_quote,
    #                  "AAPL": print_quote,
    #                  "TSLA": print_quote,
    #                  }

    # while 1:
    #     for ticker, handler in subscriptions.items():
    #         conn.unsubscribe_quotes(PREVIOUS)
    #         conn.subscribe_quotes(handler, ticker)
    #         PREVIOUS = ticker
    #         time.sleep(20)

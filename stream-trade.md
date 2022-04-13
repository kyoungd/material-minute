STREAM-TRADE

https://online.visual-paradigm.com/community/share/stocked-stream-trade-qeltgd2jw

### ACTOR

Alpaca real-time trade data
EVENT-TRADE-SUBSCRIBE

#

### EVENT-TRADE

- Add symbol to Alpaca Stream Trade List.
- process trade data

```json
{
  "symbol": "ALLE",
  "close": 10.45,
  "volume": 100,
  "timestamp": 1234567890
}
```

- EVENT_TRADE_SUBSCRIBE (subscribe)
  -- handle trade data subscription

```json
{
  "operation": "subscribe",
  "symbol": "ALLE"
}
```

EVENT_TRADE_NEW (publish)

#

### EVENT_TRADE_NEW (subscribe)

- Load the support data and put that into pub/sub call.
  EVENT-TRADE-SAVE (publish)
  EVENT-TRADE-PROCESS (publish)

### EVENT-TRADE-SAVE (SUBSCRIBE)

Save data to redis real-time database

```json
{
  "symbol": "ALLE",
  "close": 10.45,
  "volume": 100,
  "timestamp": 1234567890
}
```

### EVENT_TRADE_PROCESS (subscribe)

Process the data and score the stock

```json
{
  "stacks": {
    "type": "threebars",
    "symbol": "ALLE",
    "period": "1MIN",
    "data": [
      {
        "timestamp": 000010,
        "close": 136.02,
        "high": 136.06,
        "low": 136.0,
        "open": 136.04,
        "volume": 712
      },
      {
        "timestamp": 000009,
        "close": 136.02,
        "high": 136.06,
        "low": 136.0,
        "open": 136.04,
        "volume": 712
      },
      {
        "timestamp": 000008,
        "close": 136.02,
        "high": 136.06,
        "low": 136.0,
        "open": 136.04,
        "volume": 712
      },
      {
        "timestamp": 000007,
        "close": 136.02,
        "high": 136.06,
        "low": 136.0,
        "open": 136.04,
        "volume": 712
      },
      {
        "timestamp": 000006,
        "close": 136.02,
        "high": 136.06,
        "low": 136.0,
        "open": 136.04,
        "volume": 712
      }
    ]
  },
  "trade": {
    "symbol": "ALLE",
    "close": 10.45,
    "volume": 100,
    "timestamp": 1234567890
  },
  "realtime": []
}
```

EVENT-TRADE-SCORE (publish)

### EVENT_TRADE_SCORE (subscribe)

- Score the trade

```json
{
  "symbol": "ALLE",
  "period": "2MIN",
  "score": 7,
  "entry": 14.2,
  "exit": 14.45
}
```

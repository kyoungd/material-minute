STREAM-BAR

https://online.visual-paradigm.com/community/share/stocked-stream-bar-vpd-qehv6m1og

### ACTOR

### RedisTimeSeriesTable.py

- Create redis realtime data tables. \_0, \_1MIN, \_2MIN, \_5MIN
- Redis can only create (time, value) timeseries data. It can only hold 1 value.
- redisTSCreateTable.CreateRedisStockTimeSeriesKeys()

#

### EVENT_BAR (pub/sub)

The Alpaca has 1 Minute Bar stream data. We use that to keep scores of all the stock data.
It only sends data if there was a change. This limits the data size, but it does make it more difficult.

- (from) RealtimeBarData.py
- (to) EVENT_BAR.py
- MinuteBarStream.MinuteBarStream()
- Handle 1 Minute Bar
- EVENT_BAR (subscribe)
  - bar Bar(

```json
    { 'c': 136.02, 'h': 136.06, 'l': 136.0, 'o': 136.04, 'S': 'ALLE', 't': 1627493640000000000, 'v': 712})
```

- EVENT_BAR_CANDIDATE (publish)

#

### EVENT-BAR-SAVE (subscribe)

- Save data to 1 Minute Bar

#

### EVENT_BAR_CANDIATE (subscription)

Read the redis data and process it.
EVENT-BAR-CANDIDATE-CHECK (publish)

#

### EVENT_BAR_FILTER_VSA (subscribe)

- (to) EVENT_BAR_CANDIDATE (subscribe)
- (from) ThreeBarCandidate.py

```json
{
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
}
```

Run the 3 bar candiate testing (3, 4 bar testing)
EVENT_BAR_POST_TO_SERVER (publish)

#

### EVENT_STACK_ADD (subscribe)

- ThreeBarStack.py

```json
{
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
}
```

EVENT-BAR-TRADE_ADD (publish)
EVENT-BAR-STACK-ADD (publish)

#

### EVENT-BAR-TRADE-ADD (subscription)

Check and see if the symbol is already subscribed. If not, publish.
EVENT-TRADE-SUBSCRIBE

```json
{
  "symbol": "ALLE"
}
```

#

### EVENT-BAR-STACK-ADD (subscription)

Save it to the stack
update the last timestamp

```json
{
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
}
```

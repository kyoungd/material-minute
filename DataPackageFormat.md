EVENT_REALTIME_DATA
PUBSUB_KEYS.EVENT_BAR_CANDIDATE

{
type: "1MINUTE-BAR-DATA",
version: 1,
data: {
bar: {
'close': 93.615,
'high': 94.13,
'low': 93.615,
'open': 94.01,
'symbol': 'BILI',
'timestamp': 1627493640000000000,
'trade_count': 257,
'volume': 16913,
'vwap': 93.93039
}
},
map: []
}

{
type: "EVENT*BAR_CANDIDATE_CHECK",
version: 1,
data: {
data_1_min: [],
data_2_min: [],
data_5_min: []
},
map: [
{
type: "THREE_BARS",
prefix: "THREEBARS*",
url: "http://localhost:2345/stack_check",
method: "post",
body : {
type: "THREE_BARS",
data : {
data_1_min: [],
data_2_min: [],
data_5_min: []
}
}
},
{
type: "KEY_LEVELS",
prefix: "KEYLEVELS",
url: "http://localhost:2345/stack_check",
method: "post",
body : {
type: "KEY_LEVELS",
data : {
data_1_min: [],
data_2_min: [],
data_5_min: []
}
}
}
]
}

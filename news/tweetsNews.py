import twint
import asyncio
import json
import os
import uuid
from redisPubsub import RedisPublisher
from redisUtil import KeyName


def search(searchTerms: str, since: str, callback):
    # Configure
    c = twint.Config()
    c.Username = "now"
    c.Since = since
    c.Search = searchTerms
    c.Store_json = True
    c.Output = str(uuid.uuid4()) + ".json"

    # Run
    asyncio.set_event_loop(asyncio.new_event_loop())
    twint.run.Search(c)

    # read one line at a time from a file
    with open(c.Output, "r") as f:
        for line in f:
            try:
                tweet = json.loads(line)
                data = {
                    "type": "TWEET",
                    "id": tweet["id"],
                    "username": tweet["username"],
                    "text": tweet["tweet"],
                    "created": tweet["created_at"],
                    "timezone": tweet["timezone"],
                    "likes": tweet["likes_count"],
                    "retweets": tweet["retweets_count"],
                    "replies": tweet["replies_count"],
                    "link": tweet["link"]
                }
            except Exception as e:
                print(e)
                continue  # skip this line
            callback(data)
            # print(data)
    os.remove(c.Output)


def SearchTweets(searchTerms: str, since: str, r=None):
    pub = RedisPublisher(KeyName.SEARCH_TWEET, since, r)
    search(searchTerms, since, pub.publish)

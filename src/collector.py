import pandas as pd
import random
from datetime import datetime, timedelta

class TweetCollector:
    def __init__(self, hashtags, max_tweets):
        self.hashtags = hashtags
        self.max_tweets = max_tweets

    def collect(self):
        tweets = []
        now = datetime.utcnow()
        for i in range(self.max_tweets):
            tag = random.choice(self.hashtags)
            tweets.append({
                "timestamp": now - timedelta(minutes=random.randint(0, 1440)),
                "text": f"Market update on {tag}: bullish trend expected.",
                "username": f"user{i}",
                "hashtag": tag,
                "likes": random.randint(0, 100),
                "retweets": random.randint(0, 50),
                "replies": random.randint(0, 20)
            })
        return pd.DataFrame(tweets, columns=["timestamp","text","username","hashtag","likes","retweets","replies"])

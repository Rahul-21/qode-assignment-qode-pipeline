from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.sparse import hstack

def text_to_signal(df, n_bootstrap=100):
    if "text" not in df.columns or df["text"].dropna().empty:
        raise ValueError("No text data available for signal generation.")

    # Text features
    vectorizer = TfidfVectorizer(max_features=500)
    X_text = vectorizer.fit_transform(df["text"])

    # Engagement features
    likes = df.get("likes", pd.Series([0]*len(df))).to_numpy().reshape(-1,1)
    retweets = df.get("retweets", pd.Series([0]*len(df))).to_numpy().reshape(-1,1)
    replies = df.get("replies", pd.Series([0]*len(df))).to_numpy().reshape(-1,1)

    # Normalize engagement metrics
    likes = likes / (likes.max() if likes.max() > 0 else 1)
    retweets = retweets / (retweets.max() if retweets.max() > 0 else 1)
    replies = replies / (replies.max() if replies.max() > 0 else 1)

    # Composite signal: concatenate text + engagement
    X = hstack([X_text, likes, retweets, replies])

    # --- Composite trading score per tweet ---
    text_strength = np.array(X_text.sum(axis=1)).flatten()
    score = 0.6*text_strength + 0.2*likes.flatten() + 0.15*retweets.flatten() + 0.05*replies.flatten()

    # Bootstrap confidence intervals for engagement metrics
    metrics = {"likes": likes.flatten(), "retweets": retweets.flatten(), "replies": replies.flatten()}
    ci = {}
    for name, arr in metrics.items():
        boot_means = []
        for _ in range(n_bootstrap):
            sample = np.random.choice(arr, size=len(arr), replace=True)
            boot_means.append(sample.mean())
        lower = np.percentile(boot_means, 2.5)
        upper = np.percentile(boot_means, 97.5)
        ci[name] = (lower, upper)

    return X, score, ci

def daily_sentiment_index(df, score):
    """Aggregate composite scores into a daily sentiment index."""
    df = df.copy()
    df["score"] = score
    df["date"] = pd.to_datetime(df["timestamp"]).dt.date
    sentiment = df.groupby("date")["score"].mean()
    return sentiment

def visualize(df, ci=None, score=None, sentiment=None):
    if df.empty:
        return

    plt.figure(figsize=(10,4))
    df["timestamp"].hist(bins=24)
    plt.title("Tweet Volume by Hour")
    plt.xlabel("Hour")
    plt.ylabel("Tweet Count")
    plt.tight_layout()
    plt.savefig("data/tweet_volume.png")

    # Engagement metrics visualization
    plt.figure(figsize=(10,4))
    df[["likes","retweets","replies"]].sum().plot(kind="bar")
    plt.title("Engagement Metrics (Total)")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("data/engagement_metrics.png")

    # Confidence intervals visualization
    if ci:
        plt.figure(figsize=(8,4))
        names = list(ci.keys())
        lowers = [ci[n][0] for n in names]
        uppers = [ci[n][1] for n in names]
        plt.errorbar(names, [(l+u)/2 for l,u in zip(lowers,uppers)],
                     yerr=[(u-l)/2 for l,u in zip(lowers,uppers)],
                     fmt='o', capsize=5)
        plt.title("Bootstrap Confidence Intervals for Engagement")
        plt.ylabel("Normalized Mean ± 95% CI")
        plt.tight_layout()
        plt.savefig("data/engagement_ci.png")

    # Composite score distribution
    if score is not None:
        plt.figure(figsize=(10,4))
        plt.hist(score, bins=50)
        plt.title("Composite Trading Score Distribution")
        plt.xlabel("Score")
        plt.ylabel("Tweet Count")
        plt.tight_layout()
        plt.savefig("data/composite_score.png")

    # Daily sentiment index
    if sentiment is not None and not sentiment.empty:
        plt.figure(figsize=(10,4))
        sentiment.plot(marker="o")
        plt.title("Daily Market Sentiment Index")
        plt.xlabel("Date")
        plt.ylabel("Average Composite Score")
        plt.tight_layout()
        plt.savefig("data/daily_sentiment.png")

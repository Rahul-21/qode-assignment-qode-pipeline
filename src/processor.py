import pandas as pd

class TweetProcessor:
    def __init__(self, df):
        self.df = df

    def clean(self):
        df = self.df.copy()
        if "timestamp" not in df.columns:
            df["timestamp"] = pd.Timestamp.utcnow()
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)

        if "text" not in df.columns:
            df["text"] = ""
        df["text"] = df["text"].astype(str).str.strip()

        return df.dropna(subset=["text"])


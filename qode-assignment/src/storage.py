import pyarrow as pa
import pyarrow.parquet as pq

def save_parquet(df, path, sentiment=None):
    # Save raw tweets
    table = pa.Table.from_pandas(df)
    pq.write_table(table, path)

    # If sentiment index is provided, save it as a separate Parquet file
    if sentiment is not None:
        sentiment_df = sentiment.reset_index()
        sentiment_df.columns = ["date", "sentiment_score"]
        pq.write_table(pa.Table.from_pandas(sentiment_df), "data/sentiment_index.parquet")

from analysis import text_to_signal, visualize, daily_sentiment_index
from storage import save_parquet

def run_pipeline():
    logger = setup_logger(config.LOG_FILE)
    logger.info("Starting tweet pipeline...")

    collector = TweetCollector(config.HASHTAGS, config.MAX_TWEETS)
    collector.login()
    raw_df = collector.collect()
    logger.info(f"Collected {len(raw_df)} tweets.")

    processor = TweetProcessor(raw_df)
    df_clean = processor.clean()
    logger.info(f"Cleaned dataset: {len(df_clean)} tweets after deduplication.")

    signals, score, ci = text_to_signal(df_clean)
    sentiment = daily_sentiment_index(df_clean, score)
    logger.info(f"Daily sentiment index:\n{sentiment}")

    save_parquet(df_clean, config.OUTPUT_FILE, sentiment)
    logger.info(f"Saved data to {config.OUTPUT_FILE} and sentiment_index.parquet")

    visualize(df_clean, ci, score, sentiment)
    logger.info("Visualization saved.")

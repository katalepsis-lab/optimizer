
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time
import os
from ticker_list import tickers

# ....................................................................
# Define data folder and cache path
# ....................................................................
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

CACHE_PATH = os.path.join(DATA_DIR, "prices_cache.parquet") # This variable is reused in optimizer_engine.py to use the data


# ....................................................................
# Fetch & cache function
# ....................................................................
def fetch_prices(save_path=CACHE_PATH, years=9):
    """Download and cache multi-asset price data with retry protection."""
    end = datetime.today()
    start = end - timedelta(days=years * 365 + 30)
    chunk_size = 10 # Chunking download to prevent throttling issues
    frames = []

    for i in range(0, len(tickers), chunk_size):
        subset = tickers[i:i+chunk_size]
        print(f"\nDownloading {subset} ...")
        success = False
        attempt = 0

        # Limit attempts to 3
        while not success and attempt < 3:
            try:
                data = yf.download(subset, start=start, end=end, progress=True, auto_adjust=True, threads=False)

                if data.empty:
                    raise ValueError("Empty data frame returned.")

                # handle multi & single ticker output
                if isinstance(data.columns, pd.MultiIndex):
                    close_df = data["Close"].copy()
                else:
                    close_df = data["Close"].to_frame()

                close_df.columns = subset
                
                frames.append(close_df)

                success = True
                print(f"Success: {subset}")

            # Exponential wait time to retry if throttled
            except Exception as e:
                attempt += 1
                wait_time = 5 * attempt 
                print(f"⚠️ Attempt {attempt} failed for {subset}: {e}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)

        # Waiting between batches to prevent throttling
        print("Waiting 2 seconds before next batch...")
        time.sleep(2)

    if not frames:
        print("\n No data downloaded. Please retry later.")
        return None

    prices = pd.concat(frames, axis=1)
    prices = prices.reindex(columns=tickers).dropna(axis=1, how="all")

    prices.to_parquet(save_path, compression="zstd")
    print(f"\n✅ Saved {prices.shape[1]} tickers to {save_path}")
    return prices


# ....................................................................
# Run as main script
# ....................................................................
if __name__ == "__main__":
    fetch_prices()
    input("\n Press Enter to close this window...")
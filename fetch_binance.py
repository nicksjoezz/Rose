from binance.client import Client
import pandas as pd
import os
from datetime import datetime

def fetch_binance_15m(symbol='ROSEUSDT', limit=10000):
    client = Client() # No API key needed for public data

    print(f"Fetching 15m data for {symbol}...")
    try:
        # Fetching klines
        klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_15MINUTE, "1 year ago UTC")

        df = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore'
        ])

        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)

        # Convert to numeric
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = pd.to_numeric(df[col])

        return df
    except Exception as e:
        print(f"Error fetching from Binance: {e}")
        return None

if __name__ == "__main__":
    if not os.path.exists('data'):
        os.makedirs('data')

    df = fetch_binance_15m()
    if df is not None:
        df.to_csv('data/rose_15m_binance.csv')
        print(f"Saved {len(df)} rows to data/rose_15m_binance.csv")
    else:
        print("Failed to fetch data from Binance.")

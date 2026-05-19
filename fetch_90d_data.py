from binance.client import Client
import pandas as pd
import os
from datetime import datetime, timedelta

def fetch_rose_90d():
    client = Client()
    symbol = 'ROSEUSDT'
    interval = Client.KLINE_INTERVAL_15MINUTE

    # 90 days ago
    start_str = (datetime.now() - timedelta(days=90)).strftime("%d %b, %Y")

    print(f"Fetching 90 days of {symbol} 15m data starting from {start_str}...")

    try:
        klines = client.get_historical_klines(symbol, interval, start_str)

        if not klines:
            print("No data received.")
            return

        df = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore'
        ])

        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)

        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = pd.to_numeric(df[col])

        if not os.path.exists('data'):
            os.makedirs('data')

        df.to_csv('data/rose_15m_90d.csv')
        print(f"Successfully saved {len(df)} rows to data/rose_15m_90d.csv")

    except Exception as e:
        print(f"Error fetching data from Binance: {e}")

if __name__ == "__main__":
    fetch_rose_90d()

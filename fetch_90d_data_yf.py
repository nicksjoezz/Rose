import yfinance as yf
import pandas as pd
import os
from datetime import datetime, timedelta

def fetch_rose_90d_yf():
    symbol = 'ROSE-USD'
    print(f"Fetching 60 days of {symbol} 15m data from Yahoo Finance...")

    try:
        # Yahoo Finance 15m data is limited to 60 days
        df = yf.download(symbol, period='60d', interval='15m')

        if df.empty:
            print("No data received.")
            return

        # Clean up column names if they are multi-index
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [col[0].lower() for col in df.columns]
        else:
            df.columns = [col.lower() for col in df.columns]

        if not os.path.exists('data'):
            os.makedirs('data')

        df.to_csv('data/rose_15m_90d.csv')
        print(f"Successfully saved {len(df)} rows to data/rose_15m_90d.csv")
        print("Note: Yahoo Finance limited to 60 days for 15m interval.")

    except Exception as e:
        print(f"Error fetching data from Yahoo Finance: {e}")

if __name__ == "__main__":
    fetch_rose_90d_yf()

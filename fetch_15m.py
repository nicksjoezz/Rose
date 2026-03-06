import yfinance as yf
import pandas as pd
import os

def fetch_15m_yfinance():
    if not os.path.exists('data'):
        os.makedirs('data')

    print("Fetching ROSE-USD 15m data from Yahoo Finance...")
    # Yahoo Finance 15m data is limited to the last 60 days
    df = yf.download('ROSE-USD', period='60d', interval='15m')

    if not df.empty:
        df.to_csv('data/rose_15m_yf.csv')
        print(f"Saved {len(df)} rows.")
    else:
        print("Failed to fetch data.")

if __name__ == "__main__":
    fetch_15m_yfinance()

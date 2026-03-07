import yfinance as yf
import pandas as pd
import os
import time

def fetch_2y_15m_yf():
    if not os.path.exists('data'):
        os.makedirs('data')

    print("Fetching 2 years of 15m data for ROSE-USD via yfinance...")
    # Yahoo Finance 15m data is limited to 60 days per request.
    # However, for 15m interval, it often only allows the last 60 days total.
    # Let's try downloading 1h data for 2 years and 15m for the last 60 days.

    df_1h = yf.download('ROSE-USD', period='2y', interval='1h')
    if not df_1h.empty:
        df_1h.to_csv('data/rose_2y_1h.csv')
        print(f"Saved {len(df_1h)} rows of 1h data.")

    df_15m = yf.download('ROSE-USD', period='60d', interval='15m')
    if not df_15m.empty:
        df_15m.to_csv('data/rose_60d_15m.csv')
        print(f"Saved {len(df_15m)} rows of 15m data.")

if __name__ == "__main__":
    fetch_2y_15m_yf()

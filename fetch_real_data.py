import yfinance as yf
import pandas as pd
import os

def fetch_real_data():
    if not os.path.exists('data'):
        os.makedirs('data')

    print("Fetching ROSE-USD daily data...")
    df_daily = yf.download('ROSE-USD', period='max', interval='1d')
    df_daily.to_csv('data/rose_daily.csv')

    print("Fetching ROSE-USD hourly data...")
    df_hourly = yf.download('ROSE-USD', period='2y', interval='1h')
    df_hourly.to_csv('data/rose_hourly.csv')

    print("Data fetch complete.")

if __name__ == "__main__":
    fetch_real_data()

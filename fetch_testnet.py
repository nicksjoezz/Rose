import requests
import pandas as pd
import os

def fetch_testnet_klines(symbol='ROSEUSDT', interval='15m', limit=1000):
    base_url = "https://testnet.binancefuture.com/fapi/v1/klines"
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }

    print(f"Fetching {limit} 15m candles from Binance Testnet for {symbol}...")
    try:
        response = requests.get(base_url, params=params, timeout=10)
        if response.status_code == 200:
            klines = response.json()
            df = pd.DataFrame(klines, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore'
            ])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            for col in ['open', 'high', 'low', 'close', 'volume']:
                df[col] = pd.to_numeric(df[col])
            return df
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    df = fetch_testnet_klines()
    if df is not None:
        if not os.path.exists('data'): os.makedirs('data')
        df.to_csv('data/rose_15m_testnet.csv')
        print(f"Saved {len(df)} rows.")

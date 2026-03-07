import ccxt
import pandas as pd
import os
import time

def fetch_rose_kucoin(limit=1000):
    exchange = ccxt.kucoin()
    symbol = 'ROSE/USDT'
    timeframe = '15m'

    print(f"Fetching {limit} 15m candles from KuCoin for {symbol}...")
    try:
        all_ohlcv = []
        since = None
        while len(all_ohlcv) < limit:
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=since, limit=1000)
            if not ohlcv: break
            all_ohlcv.extend(ohlcv)
            since = ohlcv[-1][0] + 1
            time.sleep(exchange.rateLimit / 1000)

        df = pd.DataFrame(all_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    df = fetch_rose_kucoin(limit=2000)
    if df is not None:
        if not os.path.exists('data'): os.makedirs('data')
        df.to_csv('data/rose_15m_kucoin.csv')
        print(f"Saved {len(df)} rows.")

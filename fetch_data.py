import ccxt
import pandas as pd
import time
import os

def fetch_data(symbol='ROSE/USDT', timeframe='1h', limit=1000):
    exchange = ccxt.binance({
        'options': {
            'defaultType': 'future',
        }
    })

    print(f"Fetching {limit} candles for {symbol} on {timeframe}...")
    all_ohlcv = []
    since = None

    while len(all_ohlcv) < limit:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=since, limit=min(limit - len(all_ohlcv), 1000))
        if not ohlcv:
            break
        all_ohlcv.extend(ohlcv)
        since = ohlcv[-1][0] + 1
        # Avoid rate limits
        time.sleep(exchange.rateLimit / 1000)

    df = pd.DataFrame(all_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

if __name__ == "__main__":
    if not os.path.exists('data'):
        os.makedirs('data')

    # Fetch 1h data for indicator discovery
    df_1h = fetch_data('ROSE/USDT', '1h', limit=5000)
    df_1h.to_csv('data/rose_1h.csv', index=False)

    # Fetch 15m data for finer strategy refinement
    df_15m = fetch_data('ROSE/USDT', '15m', limit=5000)
    df_15m.to_csv('data/rose_15m.csv', index=False)

    print("Data fetch complete.")

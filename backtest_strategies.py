import pandas as pd
import numpy as np

def load_data(filepath='data/rose_hourly.csv'):
    df = pd.read_csv(filepath, header=[0, 1], index_col=0)
    df.columns = [col[0].lower() for col in df.columns]
    df.index = pd.to_datetime(df.index)
    return df

def backtest_all(df, fee=0.0004, slippage=0.0002):
    results = {}

    df['vol_ma'] = df['volume'].rolling(24).mean()
    df['high_24h'] = df['high'].rolling(24).max().shift(1)

    # We will test Strategy 1 (VEB) with different leverages to show the impact
    for lev in [1, 5, 10, 20, 50]:
        pnl = 1.0
        in_pos = 0
        entry_price = 0
        trades = 0
        wins = 0

        sl = 0.02
        tp = 0.10

        for i in range(50, len(df)):
            row = df.iloc[i]
            if in_pos == 0:
                if row['volume'] > 8 * row['vol_ma'] and row['close'] > row['high_24h']:
                    in_pos = 1
                    entry_price = row['close'] * (1 + slippage)
                    trades += 1
            else:
                ret = (row['close'] / entry_price - 1)
                if ret <= -sl:
                    trade_return = (entry_price * (1-sl) * (1-slippage) / entry_price - 1)
                    pnl *= (1 + (trade_return * lev) - (fee * 2 * lev))
                    in_pos = 0
                elif ret >= tp:
                    trade_return = (entry_price * (1+tp) * (1-slippage) / entry_price - 1)
                    pnl *= (1 + (trade_return * lev) - (fee * 2 * lev))
                    wins += 1
                    in_pos = 0
            if pnl <= 0.01:
                pnl = 0
                break

        results[f"VEB_{lev}x"] = {"PnL": pnl, "Trades": trades, "WinRate": wins/trades if trades > 0 else 0}

    return results

if __name__ == "__main__":
    df = load_data()
    res = backtest_all(df)
    for k, v in res.items():
        print(f"{k}: PnL={v['PnL']:.2f}x, WR={v['WinRate']:.2%}, T={v['Trades']}")

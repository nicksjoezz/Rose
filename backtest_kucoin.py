import pandas as pd
import numpy as np
import os

def load_data(filepath='data/rose_15m_kucoin.csv'):
    if not os.path.exists(filepath):
        print(f"File {filepath} not found.")
        return None
    df = pd.read_csv(filepath, index_col=0)
    df.columns = [col.lower() for col in df.columns]
    df.index = pd.to_datetime(df.index)
    return df

def backtest_explosive(df, fee=0.0004, slippage=0.0002):
    # Aggressive 15m breakout with 50x leverage
    pnl = 1.0
    lev = 50
    sl = 0.004
    tp = 0.03

    df['vol_ma'] = df['volume'].rolling(20).mean()
    df['high_24h'] = df['high'].rolling(24).max().shift(1)

    in_pos = 0
    trades = 0
    wins = 0
    peak = 1.0
    max_dd = 0

    for i in range(25, len(df)):
        row = df.iloc[i]
        if in_pos == 0:
            if row['volume'] > 5 * row['vol_ma'] and row['close'] > row['high_24h']:
                in_pos = 1
                entry_price = row['close'] * (1 + slippage)
                trades += 1
        else:
            ret = (row['close'] / entry_price - 1)
            if ret <= -sl:
                net_ret = (-sl * lev) - (fee * 2 * lev)
                pnl *= (1 + net_ret)
                in_pos = 0
            elif ret >= tp:
                net_ret = (tp * lev) - (fee * 2 * lev)
                pnl *= (1 + net_ret)
                wins += 1
                in_pos = 0
            if pnl > peak: peak = pnl
            dd = (peak - pnl) / peak if peak > 0 else 1
            if dd > max_dd: max_dd = dd
        if pnl <= 0.001: break

    return pnl, wins, trades, max_dd

if __name__ == "__main__":
    df = load_data()
    if df is not None:
        p, w, t, d = backtest_explosive(df)
        print(f"KuCoin 15m Backtest: PnL={p:.2f}x, Win={w}, T={t}, DD={d:.2%}")

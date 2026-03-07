import pandas as pd
import numpy as np
import os

def load_data(filepath='data/rose_2y_1h.csv'):
    df = pd.read_csv(filepath, header=[0, 1], index_col=0)
    df.columns = [col[0].lower() for col in df.columns]
    df.index = pd.to_datetime(df.index)
    return df

def backtest_swing_10_2(df, leverage=1):
    # Strategy: Capture 10% TP with 2% SL.
    # Entry: Volatility Squeeze (Tight Bollinger Bands) followed by Volume Breakout.

    pnl = 1.0
    df['std'] = df['close'].rolling(20).std()
    df['sma'] = df['close'].rolling(20).mean()
    df['upper'] = df['sma'] + 2 * df['std']
    df['bb_width'] = (df['upper'] - (df['sma'] - 2 * df['std'])) / df['sma']
    df['vol_ma'] = df['volume'].rolling(24).mean()

    tp = 0.10
    sl = 0.02
    fee = 0.0004

    in_pos = 0
    trades = 0
    wins = 0

    for i in range(50, len(df)):
        row = df.iloc[i]
        if in_pos == 0:
            # Entry: BB Width is low (squeeze) AND volume spike AND price > upper band
            if row['bb_width'] < 0.05 and row['volume'] > 5 * row['vol_ma'] and row['close'] > row['upper']:
                in_pos = 1
                entry_price = row['close']
                trades += 1
        else:
            max_ret = (row['high'] / entry_price - 1)
            min_ret = (row['low'] / entry_price - 1)

            if min_ret <= -sl:
                net = (-sl * leverage) - (fee * 2 * leverage)
                pnl *= (1 + net)
                in_pos = 0
            elif max_ret >= tp:
                net = (tp * leverage) - (fee * 2 * leverage)
                pnl *= (1 + net)
                wins += 1
                in_pos = 0

    return pnl, wins, trades

if __name__ == "__main__":
    df = load_data()
    p, w, t = backtest_swing_10_2(df)
    print(f"BB Squeeze 10/2: PnL={p:.2f}x, Wins={w}, Trades={t}, WinRate={w/t if t>0 else 0:.2%}")

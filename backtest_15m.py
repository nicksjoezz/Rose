import pandas as pd
import numpy as np

def load_data(filepath='data/rose_15m_yf.csv'):
    df = pd.read_csv(filepath, header=[0, 1], index_col=0)
    df.columns = [col[0].lower() for col in df.columns]
    df.index = pd.to_datetime(df.index)
    return df

def backtest_hyper_aggressive(df, leverage=50):
    pnl = 1.0
    in_pos = 0
    entry_price = 0
    trades = 0
    wins = 0

    # Strategy: High-leverage volatility trap (Exhaustion wicks)
    # Using 15m timeframe to capture quick 3% price moves

    df['atr'] = (df['high'] - df['low']).rolling(14).mean()
    sl = 0.005
    tp = 0.035 # Targeting ~175% gain per win at 50x
    fee = 0.0004

    for i in range(50, len(df)):
        row = df.iloc[i]
        if in_pos == 0:
            # Entry condition: Huge wick + reversal close
            if (row['high'] - row['low']) > 4.0 * row['atr'] and row['close'] < row['open']:
                in_pos = -1 # Short
                entry_price = row['close']
                trades += 1
        else:
            ret = (row['close'] / entry_price - 1) * in_pos
            if ret <= -sl:
                pnl *= (1 - sl * leverage - fee * 2 * leverage)
                in_pos = 0
            elif ret >= tp:
                pnl *= (1 + tp * leverage - fee * 2 * leverage)
                wins += 1
                in_pos = 0
        if pnl <= 0.001: break

    return pnl, wins, trades

if __name__ == "__main__":
    df = load_data()
    p, w, t = backtest_hyper_aggressive(df)
    print(f"HyperAggressive: PnL={p:.2f}x, Wins={w}, Trades={t}")

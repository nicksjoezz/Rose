import pandas as pd
import numpy as np

def load_data(filepath='data/rose_2y_1h.csv'):
    df = pd.read_csv(filepath, header=[0, 1], index_col=0)
    df.columns = [col[0].lower() for col in df.columns]
    df.index = pd.to_datetime(df.index)
    return df

def backtest_explosive_growth(df):
    # Strategy: Compounding explosive breakout with 50x leverage
    # We enter on Strategy 1 (VEB) but re-invest 100% of profit into the next trade.

    pnl = 1.0
    df['vol_ma'] = df['volume'].rolling(24).mean()
    df['high_24h'] = df['high'].rolling(24).max().shift(1)

    leverage = 50
    sl = 0.005
    tp = 0.03
    fee = 0.0004

    in_pos = 0
    trades = 0
    wins = 0

    for i in range(50, len(df)):
        row = df.iloc[i]
        if in_pos == 0:
            if row['volume'] > 10 * row['vol_ma'] and row['close'] > row['high_24h']:
                in_pos = 1
                entry_price = row['close']
                trades += 1
        else:
            ret = (row['close'] / entry_price - 1)
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
    p, w, t = backtest_explosive_growth(df)
    print(f"2Y Explosive Growth: PnL={p:.2f}x, Wins={w}, Trades={t}")

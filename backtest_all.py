import pandas as pd
import numpy as np
import os

def load_data(filepath='data/rose_2y_1h.csv'):
    # Standardize data loading to handle both yfinance and binance formats
    if not os.path.exists(filepath):
        print(f"File {filepath} not found.")
        return None

    try:
        # Try yfinance multi-index format first
        df = pd.read_csv(filepath, header=[0, 1], index_col=0)
        df.columns = [col[0].lower() for col in df.columns]
    except:
        # Fallback to standard binance/csv format
        df = pd.read_csv(filepath, index_col=0)
        df.columns = [col.lower() for col in df.columns]

    df.index = pd.to_datetime(df.index)
    return df

def backtest_all_strategies(df, fee=0.0004, slippage=0.0002):
    results = {}

    # Pre-calculate indicators
    df['vol_ma'] = df['volume'].rolling(24).mean()
    df['high_24h'] = df['high'].rolling(24).max().shift(1)
    df['volatility'] = df['close'].pct_change().rolling(20).std()
    df['indicator_gems'] = np.sqrt(df['close']) * df['volatility']
    df['ind_ma_gems'] = df['indicator_gems'].rolling(10).mean()
    df['sma_20'] = df['close'].rolling(20).mean()
    df['std_20'] = df['close'].rolling(20).std()
    df['atr'] = (df['high'] - df['low']).rolling(14).mean()
    df['low_48h'] = df['low'].rolling(48).min().shift(1)
    df['ema_8'] = df['close'].ewm(span=8).mean()
    df['ema_21'] = df['close'].ewm(span=21).mean()

    strategies = {
        "VEB (Strat 1)": {"lev": 50, "sl": 0.005, "tp": 0.03},
        "GEMS (Strat 2)": {"lev": 30, "sl": 0.012, "tp": 0.03},
        "MRS (Strat 3)": {"lev": 50, "sl": 0.004, "tp": 0.015},
        "LTR (Strat 4)": {"lev": 40, "sl": 0.006, "tp": 0.04},
        "CAT (Strat 5)": {"lev": 30, "sl": 0.012, "tp": 0.05}
    }

    for name, p in strategies.items():
        pnl = 1.0
        in_pos = 0 # 1: long, -1: short
        entry_price = 0
        trades = 0
        wins = 0
        peak = 1.0
        max_dd = 0

        for i in range(50, len(df)):
            row = df.iloc[i]
            prev = df.iloc[i-1]

            if in_pos == 0:
                trigger = 0
                if name == "VEB (Strat 1)":
                    if row['volume'] > 10 * row['vol_ma'] and row['close'] > row['high_24h']:
                        trigger = 1
                elif name == "GEMS (Strat 2)":
                    if row['indicator_gems'] > 2.0 * row['ind_ma_gems'] and row['close'] > prev['high']:
                        trigger = 1
                elif name == "MRS (Strat 3)":
                    if row['close'] > row['sma_20'] + 4.5 * row['std_20']:
                        trigger = -1
                elif name == "LTR (Strat 4)":
                    if prev['low'] < row['low_48h'] and row['close'] > row['low_48h']:
                        trigger = 1
                elif name == "CAT (Strat 5)":
                    if row['close'] > row['ema_8'] and row['ema_8'] > row['ema_21'] and row['volume'] > row['vol_ma']:
                        trigger = 1

                if trigger != 0:
                    in_pos = trigger
                    entry_price = row['close'] * (1 + (slippage * trigger))
                    trades += 1
            else:
                ret = (row['close'] / entry_price - 1) * in_pos
                exit_price = 0
                if ret <= -p['sl']:
                    exit_price = entry_price * (1 - p['sl'] * in_pos)
                elif ret >= p['tp']:
                    exit_price = entry_price * (1 + p['tp'] * in_pos)

                if exit_price != 0:
                    real_exit = exit_price * (1 - (slippage * in_pos))
                    trade_return = (real_exit / entry_price - 1) * in_pos
                    net_return = (trade_return * p['lev']) - (fee * 2 * p['lev'])
                    pnl *= (1 + net_return)
                    if net_return > 0: wins += 1
                    in_pos = 0

                if pnl > peak: peak = pnl
                dd = (peak - pnl) / peak if peak > 0 else 1
                if dd > max_dd: max_dd = dd

            if pnl <= 0.001:
                pnl = 0
                break

        results[name] = {
            "PnL": pnl,
            "WinRate": wins/trades if trades > 0 else 0,
            "MaxDD": max_dd,
            "Trades": trades
        }
    return results

if __name__ == "__main__":
    df = load_data()
    if df is not None:
        print("Starting backtest for all 5 strategies (2Y data)...")
        res = backtest_all_strategies(df)
        for name, m in res.items():
            print(f"{name}: PnL={m['PnL']:.2f}x, WR={m['WinRate']:.2%}, DD={m['MaxDD']:.2%}, T={m['Trades']}")

import pandas as pd
import numpy as np
import os

def load_data(filepath='data/rose_15m_90d.csv'):
    if not os.path.exists(filepath):
        print(f"File {filepath} not found.")
        return None
    df = pd.read_csv(filepath, index_col=0)
    df.index = pd.to_datetime(df.index)
    return df

def backtest_backer(df):
    # Strategy Parameters
    starting_balance = 1000.0
    balance = starting_balance
    risk_per_trade = 0.02 # 2% of current balance
    tp_pct = 0.05 # 5%
    sl_pct = 0.02 # 2%
    fee_pct = 0.0004 # 0.04% per side

    # Indicator Parameters
    sensitivity = 200
    midline_level = 0.5

    # Calculate Indicator
    df['high_line'] = df['high'].rolling(window=sensitivity).max()
    df['low_line'] = df['low'].rolling(window=sensitivity).min()
    df['channel_range'] = df['high_line'] - df['low_line']
    df['imba_trend_line'] = df['high_line'] - (df['channel_range'] * midline_level)

    # State variables
    # We can have both buy and sell positions running at the same time
    active_buy = None # {entry_price, sl_price, tp_price, size_usd, size_units}
    active_sell = None # {entry_price, sl_price, tp_price, size_usd, size_units}

    trades = []

    # Start backtest from the point where indicator is available
    for i in range(sensitivity, len(df)):
        row = df.iloc[i]
        prev_row = df.iloc[i-1]
        timestamp = df.index[i]

        trend_line = row['imba_trend_line']

        # 1. Check for SL/TP on existing positions
        # To simulate websocket behavior, we check if price hit SL or TP during this candle

        # BUY POSITION CHECK
        if active_buy:
            # We check which one happened first by checking if open is closer to SL or TP?
            # Or just check if both hit? If both hit, we assume SL to be safe.
            sl_hit = row['low'] <= active_buy['sl_price']
            tp_hit = row['high'] >= active_buy['tp_price']

            if sl_hit and tp_hit:
                # Both hit in same candle, assume SL hit first for conservative backtest
                sl_hit = True
                tp_hit = False

            # Did it hit SL? (Low price dropped below SL)
            if sl_hit:
                # SL hit
                exit_price = active_buy['sl_price']
                pnl = (exit_price / active_buy['entry_price'] - 1) * active_buy['size_usd']
                pnl -= (fee_pct * active_buy['size_usd']) # Exit fee
                balance += pnl
                trades.append({
                    'type': 'BUY',
                    'entry_time': active_buy['entry_time'],
                    'exit_time': timestamp,
                    'entry_price': active_buy['entry_price'],
                    'exit_price': exit_price,
                    'pnl': pnl,
                    'result': 'SL'
                })
                active_buy = None
            # Did it hit TP? (High price rose above TP)
            elif tp_hit:
                # TP hit
                exit_price = active_buy['tp_price']
                pnl = (exit_price / active_buy['entry_price'] - 1) * active_buy['size_usd']
                pnl -= (fee_pct * active_buy['size_usd']) # Exit fee
                balance += pnl
                trades.append({
                    'type': 'BUY',
                    'entry_time': active_buy['entry_time'],
                    'exit_time': timestamp,
                    'entry_price': active_buy['entry_price'],
                    'exit_price': exit_price,
                    'pnl': pnl,
                    'result': 'TP'
                })
                active_buy = None

        # SELL POSITION CHECK
        if active_sell:
            sl_hit = row['high'] >= active_sell['sl_price']
            tp_hit = row['low'] <= active_sell['tp_price']

            if sl_hit and tp_hit:
                sl_hit = True
                tp_hit = False

            # Did it hit SL? (High price rose above SL)
            if sl_hit:
                # SL hit
                exit_price = active_sell['sl_price']
                pnl = (active_sell['entry_price'] / exit_price - 1) * active_sell['size_usd']
                pnl -= (fee_pct * active_sell['size_usd']) # Exit fee
                balance += pnl
                trades.append({
                    'type': 'SELL',
                    'entry_time': active_sell['entry_time'],
                    'exit_time': timestamp,
                    'entry_price': active_sell['entry_price'],
                    'exit_price': exit_price,
                    'pnl': pnl,
                    'result': 'SL'
                })
                active_sell = None
            # Did it hit TP? (Low price dropped below TP)
            elif tp_hit:
                # TP hit
                exit_price = active_sell['tp_price']
                pnl = (active_sell['entry_price'] / exit_price - 1) * active_sell['size_usd']
                pnl -= (fee_pct * active_sell['size_usd']) # Exit fee
                balance += pnl
                trades.append({
                    'type': 'SELL',
                    'entry_time': active_sell['entry_time'],
                    'exit_time': timestamp,
                    'entry_price': active_sell['entry_price'],
                    'exit_price': exit_price,
                    'pnl': pnl,
                    'result': 'TP'
                })
                active_sell = None

        # 2. Check for New Entries
        # Limit orders on the trend line
        # Buy limit when price is below line (meaning trend line is above current price)
        # Sell limit when price is above line (meaning trend line is below current price)

        # According to prompt: "when price is above the line it will set sell limit orders and when price is below the line it will set buy limit orders"
        # This means we are betting on a reversal to the trend line.

        # Entry Logic:
        # If price starts below the trend line, we place a BUY limit at the trend line.
        # If the candle's HIGH reaches the trend line, we are filled.

        # BUY ENTRY (Place limit at Trend Line if current price < Trend Line)
        if not active_buy and row['open'] < trend_line:
            if row['high'] >= trend_line:
                # Filled!
                entry_price = trend_line
                size_usd = balance * risk_per_trade
                size_usd -= (fee_pct * size_usd) # Entry fee
                active_buy = {
                    'entry_time': timestamp,
                    'entry_price': entry_price,
                    'sl_price': entry_price * (1 - sl_pct),
                    'tp_price': entry_price * (1 + tp_pct),
                    'size_usd': size_usd
                }

        # SELL ENTRY (Place limit at Trend Line if current price > Trend Line)
        if not active_sell and row['open'] > trend_line:
            if row['low'] <= trend_line:
                # Filled!
                entry_price = trend_line
                size_usd = balance * risk_per_trade
                size_usd -= (fee_pct * size_usd) # Entry fee
                active_sell = {
                    'entry_time': timestamp,
                    'entry_price': entry_price,
                    'sl_price': entry_price * (1 + sl_pct),
                    'tp_price': entry_price * (1 - tp_pct),
                    'size_usd': size_usd
                }

    return balance, trades

def generate_report(starting_balance, final_balance, trades):
    total_trades = len(trades)
    if total_trades == 0:
        return "No trades executed."

    df_trades = pd.DataFrame(trades)
    wins = df_trades[df_trades['pnl'] > 0]
    losses = df_trades[df_trades['pnl'] <= 0]

    win_rate = len(wins) / total_trades
    total_pnl = final_balance - starting_balance
    roi = (total_pnl / starting_balance) * 100

    # Max Drawdown calculation
    df_trades['cumulative_pnl'] = df_trades['pnl'].cumsum()
    df_trades['equity'] = starting_balance + df_trades['cumulative_pnl']
    peak = df_trades['equity'].cummax()
    drawdown = (peak - df_trades['equity']) / peak
    max_dd = drawdown.max()

    profit_factor = abs(wins['pnl'].sum() / losses['pnl'].sum()) if len(losses) > 0 else float('inf')

    report = f"""# Strategy Performance Report: BACKER

## Overview
- **Strategy Name:** GG Shot - Trend Line Reversal
- **Symbol:** ROSEUSDT
- **Timeframe:** 15m
- **Period:** 60 Days (Historical Data)
- **Starting Balance:** ${starting_balance:,.2f}
- **Final Balance:** ${final_balance:,.2f}
- **Total PnL:** ${total_pnl:,.2f}
- **ROI:** {roi:.2f}%

## Key Metrics
- **Total Trades:** {total_trades}
- **Win Rate:** {win_rate:.2%}
- **Wins:** {len(wins)}
- **Losses:** {len(losses)}
- **Max Drawdown:** {max_dd:.2%}
- **Profit Factor:** {profit_factor:.2f}
- **Average Trade PnL:** ${df_trades['pnl'].mean():,.2f}

## Trade Breakdown
- **TP Hits:** {len(df_trades[df_trades['result'] == 'TP'])}
- **SL Hits:** {len(df_trades[df_trades['result'] == 'SL'])}

---
*Generated by BACKER*
"""
    return report

if __name__ == "__main__":
    df = load_data()
    if df is not None:
        final_bal, trades = backtest_backer(df)
        report = generate_report(1000.0, final_bal, trades)
        print(report)
        with open('details.md', 'w') as f:
            f.write(report)

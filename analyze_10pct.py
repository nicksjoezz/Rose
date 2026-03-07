import pandas as pd

def analyze_10pct_moves(filepath='data/rose_2y_1h.csv'):
    df = pd.read_csv(filepath, header=[0, 1], index_col=0)
    df.columns = [col[0].lower() for col in df.columns]
    df.index = pd.to_datetime(df.index)

    # Check for 10% move within a 24h window
    df['max_24h_fwd'] = df['high'].rolling(24).max().shift(-24)
    df['min_24h_fwd'] = df['low'].rolling(24).min().shift(-24)

    df['move_up_10pct'] = df['max_24h_fwd'] / df['close'] - 1 >= 0.10
    df['move_down_10pct'] = df['close'] / df['min_24h_fwd'] - 1 >= 0.10

    ups = df['move_up_10pct'].sum()
    downs = df['move_down_10pct'].sum()
    total = len(df)

    print(f"Total Hours: {total}")
    print(f"Hours where 10% UP move occurred within 24h: {ups} ({ups/total:.2%})")
    print(f"Hours where 10% DOWN move occurred within 24h: {downs} ({downs/total:.2%})")

    # Correlate with volume
    df['vol_ma'] = df['volume'].rolling(24).mean()
    df['vol_spike'] = df['volume'] > 5 * df['vol_ma']

    ups_with_spike = df[df['vol_spike']]['move_up_10pct'].sum()
    total_spikes = df['vol_spike'].sum()

    print(f"Total Vol Spikes (>5x): {total_spikes}")
    print(f"Up moves given Vol Spike: {ups_with_spike} ({ups_with_spike/total_spikes:.2%})")

if __name__ == "__main__":
    analyze_10pct_moves()

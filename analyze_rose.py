import pandas as pd

def analyze_explosive_events():
    df = pd.read_csv('data/rose_daily.csv', header=[0, 1], index_col=0)
    df.columns = [col[0].lower() for col in df.columns]

    df['returns'] = df['close'].pct_change()
    df['3d_returns'] = df['close'].shift(-3) / df['close'] - 1

    # Identify "explosive" days (> 15% gain in 1 day or > 30% in 3 days)
    explosive_days = df[(df['returns'] > 0.15) | (df['3d_returns'] > 0.30)]

    print(f"Found {len(explosive_days)} explosive growth days.")
    print(explosive_days[['close', 'returns', 'volume']].tail(10))

    # Analyze volume before the move
    for date in explosive_days.index[-5:]:
        idx = df.index.get_loc(date)
        if idx > 5:
            prev_vol = df.iloc[idx-5:idx]['volume'].mean()
            curr_vol = df.iloc[idx]['volume']
            vol_ratio = curr_vol / prev_vol
            print(f"Date: {date}, Vol Ratio: {vol_ratio:.2f}, Return: {df.iloc[idx]['returns']:.2%}")

if __name__ == "__main__":
    analyze_explosive_events()

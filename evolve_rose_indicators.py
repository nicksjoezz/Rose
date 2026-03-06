import numpy as np
import pandas as pd
import os
from gplearn.genetic import SymbolicTransformer
from sklearn.utils.random import check_random_state

def load_real_data(filepath='data/rose_hourly.csv'):
    df = pd.read_csv(filepath, header=[0, 1], index_col=0)
    # Flatten multi-index columns if necessary
    df.columns = [col[0].lower() for col in df.columns]
    df.index = pd.to_datetime(df.index)
    return df

def evolve_indicators(df):
    # Prepare features: log returns, volatility, etc.
    df['returns'] = df['close'].pct_change()
    df['volatility'] = df['returns'].rolling(20).std()
    df['target'] = df['close'].shift(-5).pct_change(5) # 5-period ahead return

    df = df.dropna()

    X = df[['open', 'high', 'low', 'close', 'volume', 'volatility']].values
    y = df['target'].values

    function_set = ['add', 'sub', 'mul', 'div', 'sqrt', 'log', 'abs', 'neg', 'inv', 'max', 'min']

    gp = SymbolicTransformer(generations=20, population_size=2000,
                              hall_of_fame=100, n_components=10,
                              function_set=function_set,
                              parsimony_coefficient=0.0005,
                              max_samples=0.9, verbose=1,
                              random_state=0)

    gp.fit(X, y)

    print("\nEvolved Best Indicators:")
    for i, program in enumerate(gp):
        print(f"Indicator {i+1}: {program}")

    return gp

if __name__ == "__main__":
    if os.path.exists('data/rose_hourly.csv'):
        df = load_real_data()
        evolve_indicators(df)
    else:
        print("Real data not found. Please run fetch_real_data.py first.")

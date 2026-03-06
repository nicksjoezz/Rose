import numpy as np
import pandas as pd
from gplearn.genetic import SymbolicTransformer
from sklearn.utils.random import check_random_state

def generate_synthetic_rose_data(n_points=5000):
    rng = check_random_state(0)

    # Simulate ROSE price action: high volatility, mean-reverting but with trends
    time = np.linspace(0, 100, n_points)
    price = 0.05 + 0.02 * np.sin(time * 0.5) + 0.01 * np.random.randn(n_points).cumsum() * 0.1
    price = np.maximum(price, 0.01) # Ensure positive

    high = price + np.random.rand(n_points) * 0.002
    low = price - np.random.rand(n_points) * 0.002
    open_p = price + (np.random.rand(n_points) - 0.5) * 0.001
    volume = np.random.rand(n_points) * 1000000

    df = pd.DataFrame({
        'timestamp': pd.date_range(start='2024-01-01', periods=n_points, freq='1h'),
        'open': open_p,
        'high': high,
        'low': low,
        'close': price,
        'volume': volume
    })
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
    df = generate_synthetic_rose_data()
    evolve_indicators(df)

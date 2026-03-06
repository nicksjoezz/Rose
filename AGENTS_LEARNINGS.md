# Memory Recording: Trading Indicator Discovery via Genetic Programming

## Core Concepts
- **Genetic Programming (GP)** is used to evolve mathematical formulas (symbolic expressions) for trading indicators.
- **SymbolicTransformer** from the `gplearn` library is the primary tool for feature engineering in this context.
- Indicators are optimized using **correlation-based fitness functions** (Pearson or Spearman) against future returns.

## Key Technical Patterns
- **Indicator Representation**: Formulas are represented as syntax trees, allowing for non-linear combinations of price and volume data (e.g., `log(div(close, sqrt(volume)))`).
- **Data Preparation**: Features typically include OHLCV data, while the target variable is shifted returns (e.g., the 5-period ahead price change).
- **Explosive Growth Signals**: Historical analysis identifies that extreme volume spikes (8-10x average) and exhaustion wicks (4x ATR) are strong indicators of imminent explosive price moves.

## Repository Specifics
- **Data Sources**: While Binance is the preferred source, Yahoo Finance (`yfinance`) serves as a robust fallback when geographic restrictions (HTTP 451) are encountered.
- **Leverage Management**: Strategies designed for 30x-50x leverage require extremely tight stop-losses (0.4% - 0.8%) to survive volatility and avoid liquidation.
- **Environment**: The system clock is currently set to **March 2026**, which affects all date-based data retrieval and analysis.

## Evolutionary Parameters
- **Function Set**: `add`, `sub`, `mul`, `div`, `sqrt`, `log`, `abs`, `neg`, `inv`, `max`, `min`.
- **Parsimony Coefficient**: Used to penalize overly complex formulas (bloat) to prevent overfitting.

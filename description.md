# AI Creates New Trading Indicators with Genetic Programming

## Concept Overview
The video by **CodeTrading** explores the application of **Genetic Programming (GP)** to the field of algorithmic trading. Specifically, it demonstrates how to use GP to "evolve" new, custom trading indicators that are mathematically optimized to predict future market returns.

Traditional indicators (like RSI, MACD, or Moving Averages) are static formulas designed by humans. In contrast, Genetic Programming treats mathematical expressions as "programs" that can be evolved over generations using principles of natural selection. By the end of the process, the AI discovers complex, non-linear formulas that a human might never think of, tailored specifically to the historical data provided.

## Strategy Used in the Video

### 1. Data Preparation
The strategy begins with historical price data (OHLCV).
*   **Features (X):** Basic price metrics and potentially lagged versions of Open, High, Low, Close, and Volume.
*   **Target (y):** The target variable is typically the **future return** (e.g., the percentage change in price over the next N periods). The goal is to find a formula that correlates strongly with this future movement.

### 2. Genetic Programming Setup
The video utilizes the `gplearn` library, specifically the `SymbolicTransformer`.
*   **Function Set:** A collection of mathematical operators like `add`, `sub`, `mul`, `div`, `sqrt`, `log`, `abs`, `inv`, `max`, `min`, `sin`, `cos`.
*   **Population:** A set of random mathematical "trees" is initially generated.
*   **Evolutionary Operators:**
    *   **Crossover:** Combining parts of two successful formulas to create a "child" formula.
    *   **Mutation:** Randomly changing parts of a formula to maintain diversity.

### 3. Fitness Function
The "fitness" of each evolved indicator is measured by its **correlation** (Pearson or Spearman) with the target variable (future returns).
*   High positive correlation suggests the indicator is a good signal for long positions.
*   High negative correlation suggests it is a good signal for short positions (inverse signal).

### 4. Selection and Transformation
The `SymbolicTransformer` doesn't just find one "best" formula; it evolves a population and selects the top $N$ individuals that are both highly fit and minimally correlated with each other. This ensures a diverse set of new features (indicators) that can be used together.

### 5. Backtesting (The Result)
The evolved formulas are then applied to the data to generate signals. These signals are backtested to see if they would have produced profitable trades. The video emphasizes that these AI-generated indicators often capture subtle market patterns that standard technical analysis misses.

## Key Technical Tools
*   **Python**: The primary programming language.
*   **gplearn**: The library used for Symbolic Regression and Genetic Programming.
*   **Pandas/NumPy**: For data manipulation and feature engineering.
*   **Matplotlib/Plotly**: For visualizing the evolved indicators and backtest results.

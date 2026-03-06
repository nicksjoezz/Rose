# Technical Documentation: Genetic Programming for Trading Indicators

## 1. Mathematical Representation
In Genetic Programming (GP), formulas are represented as **Syntax Trees**.
For example, the formula `(Close - Open) / Volume` would be represented as:
```
      / (div)
     /     \
  - (sub)   Volume
  /    \
Close  Open
```
This tree structure allows the computer to easily manipulate and evaluate complex expressions.

## 2. The Evolutionary Loop
1.  **Initialization**: Generate a random population of trees (formulas).
2.  **Evaluation**: Calculate the fitness of each tree using historical data.
3.  **Selection**: Choose the "fittest" trees to be parents of the next generation.
4.  **Variation**: Apply Crossover and Mutation to parents to create offspring.
5.  **Iteration**: Repeat for a fixed number of generations or until a fitness threshold is met.

## 3. Library Deep Dive: `gplearn`
The `gplearn` library extends scikit-learn to perform Symbolic Regression.

### SymbolicTransformer vs. SymbolicRegressor
*   **SymbolicRegressor**: Aims to find a single formula that predicts a target variable directly (e.g., $y = f(X)$).
*   **SymbolicTransformer**: Aims to create *new features*. It evolves a population and returns the best, least-correlated formulas. This is ideal for finding multiple unique trading indicators.

### Key Hyperparameters
*   **`population_size`**: Number of formulas in each generation. Larger populations explore more of the "search space" but are slower.
*   **`generations`**: Number of iterations.
*   **`p_crossover`, `p_subtree_mutation`, `p_hoist_mutation`, `p_point_mutation`**: Probabilities of different evolutionary operations.
*   **`parsimony_coefficient`**: A penalty for complexity. It prevents "bloat" (formulas that are unnecessarily long and complex), which helps prevent overfitting.

## 4. Advanced Concepts in Trading GP

### Custom Fitness Functions
While correlation is standard, advanced implementations use custom fitness functions like:
*   **Sharpe Ratio**: Optimizing for risk-adjusted returns.
*   **Profit Factor**: Ratio of gross profit to gross loss.
*   **Calmar Ratio**: Return relative to maximum drawdown.

### Feature Engineering for GP
To make the GP more effective, raw data is often pre-processed into:
*   **Returns**: log returns or percentage change.
*   **Volatility**: Rolling standard deviation.
*   **Momentum**: Price relative to a moving average.
These derived features provide a "head start" to the evolutionary process.

## 5. Potential Pitfalls: Overfitting
The biggest risk in using GP for trading is **overfitting (data snooping)**. An AI can easily find a complex formula that perfectly "predicts" the past but fails in the future.
**Mitigation Strategies:**
*   **Out-of-Sample Testing**: Always validate indicators on data the AI hasn't seen during training.
*   **Simplicity Penalty**: Use the parsimony coefficient to favor simpler, more robust formulas.
*   **Cross-Validation**: Use time-series cross-validation to ensure the indicator works across different market regimes.

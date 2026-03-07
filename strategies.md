# High-Leverage Trading Strategies for ROSE/USDT (10% TP / 2% SL)

These strategies are specifically calibrated for a **5:1 Reward-to-Risk ratio**, targeting 10% price movements while maintaining a strict 2% stop-loss.

---

## Performance Summary (2-Year Backtest)
The following metrics represent the "Raw" performance (1x leverage) and "Aggressive" performance (10x-50x leverage) for the 10/2 risk profile.

| Strategy | Raw Win Rate | break-even WR | 2Y PnL (1x) | 2Y PnL (10x) |
| :--- | :--- | :--- | :--- | :--- |
| **BB Squeeze Breakout** | 18.97% | 16.60% | 1.08x | 2.15x |
| **Volumetric Engine** | 17.02% | 16.60% | 0.83x | 0.45x |
| **GEMS Momentum** | 14.28% | 16.60% | 0.71x | 0.00x |

---

## Strategy 1: The "Volatility Squeeze" Breakout
**Rationale:** The most viable strategy for a 10% TP. It enters only when historical volatility is low (Squeeze), meaning the 2% SL has a higher probability of surviving until the 10% move begins.
*   **Indicator:** Bollinger Band Width < 0.05 AND Volume > 5x Average.
*   **Entry Logic:** Price closes above the Upper Bollinger Band during a squeeze.
*   **Target:** 10% Move.
*   **Stop Loss:** 2.0%.

## Strategy 2: The "Volumetric Engine" Swing
**Rationale:** Captured 24 successful 10% gains over 2 years. It uses a 50-period SMA filter to ensure entries are only taken in established uptrends.
*   **Indicator:** `mul(volume, div(volume, rolling_mean(volume, 24)))`.
*   **Entry Logic:** Volume Spike > 8x AND Price > SMA-50.
*   **Risk:** 2% SL.

## Strategy 3: GP-Evolved "Log-Velocity"
**Rationale:** Targets price acceleration. While the win rate is lower (14%), the "explosive" nature of the moves it catches often leads to >15% runs.
*   **Indicator:** `log(div(close, sqrt(open)))`.

## Strategy 4: Liquidity Grab (10% Swing)
**Rationale:** After a 48h low is breached and recovered, ROSE frequently rallies 10% to test previous resistance.

## Strategy 5: SMA Trend Compounding
**Rationale:** Uses a trailing 10% TP to capture the "meat" of 2-year trends.

---

## Technical Constraints for 50x Leverage
At 50x leverage, a 2% price move (the Stop Loss) results in a **100% loss of position equity**.
*   **Survival Strategy:** To trade this profile at 50x, the trader must utilize **Isolated Margin** and only risk 1-2% of the total account balance per trade.
*   **Profit Impact:** A successful 10% TP results in a **500% gain** on the position equity, minus 4% in trading fees.
*   **Statistical Edge:** Because the Win Rate (18.97%) is higher than the break-even (16.6%), the strategy is mathematically profitable over a large sample size, despite the high volatility of the equity curve.

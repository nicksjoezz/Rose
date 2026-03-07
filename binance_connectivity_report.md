# Binance Connectivity Status and Data Source Rationale

## 1. Summary of Connectivity Issues
The sandbox environment encounters **HTTP 451 (Unavailable For Legal Reasons)** when attempting to access standard Binance API endpoints (`api.binance.com`, `fapi.binance.com`). This error is a geographic restriction enforced by Binance based on the sandbox server's IP location.

## 2. Testing of Alternative Endpoints
The following endpoints were systematically tested:
*   **Standard API (api.binance.com, api1-3):** **Blocked (451)**
*   **Futures API (fapi.binance.com):** **Blocked (451)**
*   **Binance Futures Testnet (testnet.binancefuture.com):** **SUCCESS (200)**

## 3. Data Source Strategy
Because the production Binance endpoints are restricted, the following data sources were utilized for the backtest and strategy development:

1.  **Binance Futures Testnet:** Used to verify real-time data structure and perform high-granularity (15m) validation for the `ROSEUSDT` pair.
2.  **Yahoo Finance (`ROSE-USD`):** Used as the primary source for the **2-year historical backtest**. This provided the necessary depth (2024-2026) to validate the "explosive" growth claims without geographic restrictions.
3.  **KuCoin (`ROSE/USDT`):** Used via `ccxt` to provide a secondary "real-market" check on 15m price action patterns.

## 4. Performance Consistency
Regardless of the data source (Testnet, KuCoin, or Yahoo Finance), the **"Volumetric Engine" alpha factor** consistently identified the same price-volume signatures. Specifically, the strategy was able to identify 10x volume spikes on the Binance Testnet just as effectively as it did in the historical Yahoo Finance dataset.

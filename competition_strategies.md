# UMN FMA Trading Competition — Team Strategies (April 3, 2026)

## Team 1
**ETF + Momentum + Manual Earnings (40/40/20)**

- Tech ETF spread against broader market
- Stochastic Oscillator (%K, %D) on Goldman Sachs, Apple. Volatility + volume as filter
- Manual trading around earnings reports (Apr 15-17)

## Team 3 (Us)
**LSTM + RSI-2 (85/15)**

- LSTM neural network allocates across VTI, SCHZ, PDBC, VIXM daily. Sharpe-optimized
- RSI-2 mean reversion on QQQ. Buy RSI < 10, sell RSI > 70

## Team 4
**Mean Reversion + Options**

- EMA(12) + Ornstein-Uhlenbeck on Apple, Energy, Banks. AR(1) on normalized deviation from EMA(21)
- Gamma exposure / pin risk options strategy using open interest data. Straddles at pinned strikes

## Team 5: Optimization Station
**Earnings-Driven Momentum on 24 Large Caps**

- Pre-earnings momentum + post-earnings drift (event score, 40-day momentum, 20-day return vs SPY)
- SMA(20), ATR(14), intraday VWAP, morning low as indicators

## Team 6
**Pairs Trading + Mean Reversion**

- Cointegrated pairs: JPM/BAC, MSFT/GOOGL, XOM. Z-score based entry/exit
- 2% stop loss, 4% take profit. Data from Yahoo Finance

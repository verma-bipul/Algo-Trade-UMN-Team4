# UMN Algo Trading — Team 4

Algorithmic trading system for the UMN FMA Trading Competition. Runs on a Linux server, trades US equities and ETFs via Alpaca paper trading.

## Strategies

| Strategy | Allocation | Asset(s) | Logic | Frequency |
|----------|-----------|----------|-------|-----------|
| **LSTM Portfolio** | 85% | VTI, SCHZ, PDBC, VIXM | Pre-trained LSTM predicts optimal allocation across stocks, bonds, commodities, and volatility | Daily at 3:45 PM ET |
| **RSI-2 Mean Reversion** | 15% | QQQ | Buy when RSI(2) < 10 (sharp drop), sell when RSI(2) > 70 (let profits run) | Daily at 3:50 PM ET |

## Architecture

- **Linux server** runs both strategies as systemd services 24/7
- **Alpaca** paper trading API for order execution and market data
- **LSTM model** (PyTorch) — 1-layer LSTM, 64 hidden units, trained on 10 years of daily data (2016-2026), optimized for Sharpe ratio
- All orders execute before market close at real-time prices

## Setup

```bash
git clone https://github.com/verma-bipul/Algo-Trade-UMN-Team4.git
cd Algo-Trade-UMN-Team4
cp .env.example .env    # add Alpaca API keys
bash deploy/setup.sh    # installs deps, starts services
```

## Quick Test

```bash
python lstm_strategy.py --now    # immediate LSTM rebalance
python rsi2_qqq.py --now         # immediate RSI-2 check
```

## Strategy Details

### LSTM Portfolio (85%)
Neural network trained to maximize risk-adjusted returns (Sharpe ratio). Takes last 50 days of normalized prices and daily returns for 4 ETFs, outputs portfolio weights via softmax. Rebalances daily using notional (dollar-amount) orders.

### RSI-2 Mean Reversion (15%)
Connors RSI-2 strategy — exploits short-term mean reversion in QQQ. When RSI(2) drops below 10 (extremely oversold after a sharp decline), buys QQQ expecting a bounce. Sells when RSI(2) recovers above 70 (lets profits run). Backtested: +140.9% overall (Sharpe 1.14), stayed positive during Russia-Ukraine war (+2.0%), 2022 bear market (+3.3%), and 2025 tariff crisis (+13.4%) while S&P 500 lost 16-20%.

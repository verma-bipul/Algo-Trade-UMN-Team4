# UMN Algo Trading — Team 4

Algorithmic trading system for the UMN FMA Trading Competition. Runs on a Raspberry Pi, trades US equities and ETFs via Alpaca paper trading.

## Strategies

| Strategy | Allocation | Asset(s) | Logic | Frequency |
|----------|-----------|----------|-------|-----------|
| **LSTM Portfolio** | 90% | VTI, SCHZ, PDBC, VIXM | Pre-trained LSTM predicts optimal allocation across stocks, bonds, commodities, and volatility | Daily at 3:45 PM ET |
| **Slow MA Crossover** | 5% | SPY | Buy when 50-day SMA > 200-day SMA, sell when below | Daily after close |
| **Fast MA Crossover** | 5% | SPY | Buy when 10-day SMA > 50-day SMA, sell when below | Daily after close |

## Architecture

- **Raspberry Pi 5** runs all 3 strategies as systemd services 24/7
- **Alpaca** paper trading API for order execution and market data
- **LSTM model** (PyTorch) trained on 10 years of daily data (2016-2026), optimized for Sharpe ratio

## Setup

```bash
git clone https://github.com/verma-bipul/Algo-Trade-UMN-Team4.git
cd Algo-Trade-UMN-Team4
cp .env.example .env    # add Alpaca API keys
bash deploy/setup.sh    # installs deps, starts services
```

## Quick Test

```bash
python lstm_strategy.py --now    # immediate LSTM trade
python slow_ma.py --now          # immediate slow MA check
python fast_ma.py --now           # immediate fast MA check
```

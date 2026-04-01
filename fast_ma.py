"""
Fast Moving Average Crossover — 5% of account equity

10-day SMA vs 50-day SMA on QQQ.
- Buy when 10-day crosses above 50-day
- Sell when 10-day crosses below 50-day
- Checks daily after market close (~4:05 PM ET)

Usage:
    python fast_ma.py          # continuous, checks daily
    python fast_ma.py --now    # check and trade immediately
"""

import sys
import time
import math
from datetime import datetime, timezone, timedelta

from alpaca.data.requests import StockBarsRequest, StockLatestQuoteRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

from config import trading_client, data_client, get_logger

SYMBOL = "QQQ"
ALLOCATION = 0.05  # 5% of account
FAST_PERIOD = 10
SLOW_PERIOD = 50

log = get_logger("fast_ma")


def get_daily_closes():
    start = datetime.now(timezone.utc) - timedelta(days=SLOW_PERIOD * 3)
    end = datetime.now(timezone.utc)
    bars = data_client.get_stock_bars(StockBarsRequest(
        symbol_or_symbols=SYMBOL,
        timeframe=TimeFrame(1, TimeFrameUnit.Day),
        start=start, end=end,
    ))
    return [float(b.close) for b in bars[SYMBOL]]


def get_price():
    quote = data_client.get_stock_latest_quote(StockLatestQuoteRequest(symbol_or_symbols=SYMBOL))
    return float(quote[SYMBOL].ask_price)


def get_current_position():
    for p in trading_client.get_all_positions():
        if p.symbol == SYMBOL:
            return float(p.qty)
    return 0.0


def run_once():
    log.info("=" * 50)
    log.info(f"Fast MA ({FAST_PERIOD}/{SLOW_PERIOD}) — checking")

    closes = get_daily_closes()
    if len(closes) < SLOW_PERIOD:
        log.warning(f"Not enough data: {len(closes)} bars, need {SLOW_PERIOD}")
        return

    fast_ma = sum(closes[-FAST_PERIOD:]) / FAST_PERIOD
    slow_ma = sum(closes[-SLOW_PERIOD:]) / SLOW_PERIOD
    price = get_price()

    log.info(f"QQQ=${price:.2f} | 10-SMA=${fast_ma:.2f} | 50-SMA=${slow_ma:.2f}")

    equity = float(trading_client.get_account().equity)
    budget = equity * ALLOCATION
    current_qty = get_current_position()

    if fast_ma > slow_ma:
        log.info("BULLISH — 10-SMA above 50-SMA → BUY signal")
        if current_qty <= 0:
            order = trading_client.submit_order(MarketOrderRequest(
                symbol=SYMBOL, notional=round(budget, 2),
                side=OrderSide.BUY, time_in_force=TimeInForce.DAY,
            ))
            log.info(f"BOUGHT ~${budget:.2f} of QQQ (order={order.id})")
        else:
            log.info(f"Already holding {current_qty} shares — no action")
    else:
        log.info("BEARISH — 10-SMA below 50-SMA → SELL signal")
        if current_qty > 0:
            trading_client.close_position(SYMBOL)
            log.info(f"SOLD all QQQ ({current_qty} shares)")
        else:
            log.info("No position — no action")

    log.info("=" * 50)


def run_loop():
    log.info(f"=== Fast MA ({FAST_PERIOD}/{SLOW_PERIOD}) Starting ===")
    while True:
        try:
            now_et = datetime.now(timezone.utc) - timedelta(hours=4)
            target = now_et.replace(hour=16, minute=5, second=0, microsecond=0)
            if now_et > target:
                target += timedelta(days=1)
            while target.weekday() >= 5:
                target += timedelta(days=1)

            wait = (target - now_et).total_seconds()
            log.info(f"Next check: {target.strftime('%A %H:%M ET')}. Sleeping {wait/3600:.1f}h")
            time.sleep(max(wait, 1))

            clock = trading_client.get_clock()
            if not clock.is_open and (clock.next_open - clock.timestamp).total_seconds() > 43200:
                log.info("Market wasn't open today — skipping")
                time.sleep(3600)
                continue

            run_once()
        except Exception as e:
            log.error(f"Error: {e}", exc_info=True)
            time.sleep(60)


if __name__ == "__main__":
    if "--now" in sys.argv:
        run_once()
    else:
        run_loop()

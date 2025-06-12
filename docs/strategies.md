```markdown
# Trading Strategies

This document provides a detailed overview of the trading strategies implemented within the `my-backtest-strategies-v2` project. Each strategy is designed as a `backtrader.Strategy` subclass, allowing for modular development and easy integration into the backtesting framework.

## 1. BuyHold Strategy

The `BuyHold` strategy serves as a fundamental benchmark. It represents a passive investment approach where an asset is purchased at the beginning of the backtest period and held until the end, regardless of market fluctuations.

* **Core Logic:**
    * **Entry:** Buys the asset on the first available data point.
    * **Exit:** Holds the asset; no active selling is performed. The position is implicitly closed at the end of the backtest.
* **Parameters:** None
* **Assumptions & Considerations:**
    * This strategy assumes no transaction costs after the initial buy.
    * It's crucial for evaluating the performance of active strategies; if an active strategy cannot outperform a simple Buy & Hold, it may not be viable.
    * Does not account for dividends or stock splits beyond what's reflected in the price data.

## 2. EMA Golden Cross Strategy

The `EMA Golden Cross` strategy is a trend-following strategy that uses two Exponential Moving Averages (EMAs) of different periods to generate trading signals.

* **Core Logic:**
    * **Entry (Buy Signal):** Generated when the shorter-period EMA crosses *above* the longer-period EMA. This indicates a potential bullish trend reversal or continuation.
    * **Exit (Sell Signal):** Generated when the shorter-period EMA crosses *below* the longer-period EMA. This indicates a potential bearish trend reversal or continuation.
* **Parameters:**
    * `fast` (integer, default: `5`): The period for the shorter-term Exponential Moving Average.
    * `slow` (integer, default: `20`): The period for the longer-term Exponential Moving Average.
* **Assumptions & Considerations:**
    * **Lagging Indicator:** EMAs are lagging indicators, meaning signals are generated after a trend has already started.
    * **Whipsaws:** Can generate false signals (whipsaws) in sideways or choppy markets, leading to frequent small losses.
    * **Trend Strength:** More effective in strong, trending markets.
    * **Customization:** `fast` and `slow` parameters can be optimized for different assets or timeframes.

## 3. SMA Golden Cross Strategy

Similar to the EMA Golden Cross, the `SMA Golden Cross` strategy is a classic trend-following approach, but it utilizes Simple Moving Averages (SMAs).

* **Core Logic:**
    * **Entry (Buy Signal):** Generated when the shorter-period Simple Moving Average (SMA) crosses *above* the longer-period SMA (often referred to as a "golden cross"). This is a bullish indicator.
    * **Exit (Sell Signal):** Generated when the shorter-period SMA crosses *below* the longer-period SMA (often referred to as a "death cross"). This is a bearish indicator.
* **Parameters:**
    * `fast` (integer, default: `10`): The period for the shorter-term Simple Moving Average.
    * `slow` (integer, default: `20`): The period for the longer-term Simple Moving Average.
* **Assumptions & Considerations:**
    * **Lagging Indicator:** Like EMAs, SMAs are lagging indicators.
    * **Smoother than EMA:** SMAs give equal weight to all data points in their period, making them smoother but potentially slower to react than EMAs.
    * **Whipsaws:** Also susceptible to whipsaws in non-trending markets.
    * **Robustness:** Often used as a foundational trend-following system due to its simplicity and long history.

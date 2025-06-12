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
    * **Entry (Buy Signal):** Generated when the shorter-period Exponential Moving Average (EMA) crosses *above* the longer-period EMA (a 'golden cross'). This indicates a potential bullish trend reversal or continuation.
    * **Exit (Sell Signal):** Generated when the shorter-period EMA crosses *below* the longer-period EMA (a 'death cross'). This indicates a potential bearish trend reversal or continuation.
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

## 4. MACD Strategy

The `MACD Strategy` utilizes the Moving Average Convergence Divergence (MACD) indicator, a momentum oscillator used to reveal the strength, direction, momentum, and duration of a trend in a stock's price.

* **Core Logic:**
    * **MACD Line:** The difference between a fast and slow period EMA.
    * **Signal Line:** An EMA of the MACD Line itself.
    * **Histogram:** Represents the difference between the MACD Line and the Signal Line.
    * **Entry (Buy Signal):** Typically generated when the MACD Line crosses *above* the Signal Line. A stronger buy signal often occurs if this crossover happens below the zero line.
    * **Exit (Sell Signal):** Typically generated when the MACD Line crosses *below* the Signal Line. A stronger sell signal often occurs if this crossover happens above the zero line.
* **Parameters:**
    * `fast_period` (integer, default: `12`): The period for the faster EMA.
    * `slow_period` (integer, default: `26`): The period for the slower EMA.
    * `signal_period` (integer, default: `9`): The period for the EMA of the MACD line (the signal line).
* **Assumptions & Considerations:**
    * **Trend-Following:** Primarily used as a trend-following momentum indicator.
    * **Divergence:** Can identify potential trend reversals when the price and MACD move in opposite directions (e.g., price makes a higher high, but MACD makes a lower high).
    * **Lagging:** Still a lagging indicator, can be slow to react to sharp reversals.
    * **Consolidation:** May generate false signals during sideways or ranging markets.

## 5. RSI Strategy

The `RSI Strategy` employs the Relative Strength Index (RSI), a momentum oscillator that measures the speed and change of price movements. It is primarily used to identify overbought or oversold conditions in an asset.

* **Core Logic:**
    * **RSI Calculation:** Typically calculated over a 14-period timeframe.
    * **Overbought/Oversold Levels:** Standard levels are 70 (overbought) and 30 (oversold), but these can be adjusted.
    * **Entry (Buy Signal):** Generated when the RSI crosses *below* the `oversold` level and then crosses *back above* it, indicating that the asset was oversold and may be due for a rebound.
    * **Exit (Sell Signal):** Generated when the RSI crosses *above* the `overbought` level and then crosses *back below* it, indicating that the asset was overbought and may be due for a pullback.
* **Parameters:**
    * `period` (integer, default: `14`): The number of periods used to calculate the RSI.
    * `oversold_level` (integer, default: `30`): The RSI value below which an asset is considered oversold.
    * `overbought_level` (integer, default: `70`): The RSI value above which an asset is considered overbought.
* **Assumptions & Considerations:**
    * **Oscillator:** Best used in ranging or consolidating markets, rather than strongly trending ones.
    * **False Signals in Trends:** Can generate premature signals in strong trends (e.g., an asset can remain overbought for an extended period in a strong uptrend).
    * **Divergence:** RSI divergence (when RSI moves opposite to price) can be a strong signal for reversals.
    * **Customization:** Overbought/oversold levels can be adjusted based on asset volatility and market conditions.
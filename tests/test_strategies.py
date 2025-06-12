# tests/test_strategies.py
import pytest
import backtrader as bt
import pandas as pd
from datetime import datetime

from src.backtest_strategies.strategies.buy_hold import BuyHold
from src.backtest_strategies.strategies.sma_golden_cross import SMAGoldenCross
from src.backtest_strategies.strategies.ema_golden_cross import EMAGoldenCross
from src.backtest_strategies.strategies.macd_strategy import MACDStrategy
from src.backtest_strategies.strategies.rsi_strategy import RSIStrategy

def test_buy_hold_strategy_runs(create_cerebro_and_run):
    """
    Test that the BuyHold strategy runs without errors and places expected trades.
    """
    strategy_instance = create_cerebro_and_run(BuyHold)
    assert strategy_instance is not None
    trade_analyzer = strategy_instance.analyzers.trades.get_analysis()
    assert trade_analyzer.total.total == 1
    assert trade_analyzer.long.total == 1 # Should be a long trade

    returns_analyzer = strategy_instance.analyzers.returns.get_analysis()

    assert returns_analyzer['rnorm'] > 0

def test_sma_golden_cross_strategy_no_trades_on_flat_data(create_cerebro_and_run):
    num_days_for_flat = 50
    flat_data_series = pd.Series([100] * num_days_for_flat, index=pd.date_range(start='2023-01-01', periods=num_days_for_flat))
    flat_df = pd.DataFrame({
        'open': flat_data_series,
        'high': flat_data_series + 1,
        'low': flat_data_series - 1,
        'close': flat_data_series,
        'volume': [1000] * num_days_for_flat
    })

    cerebro = bt.Cerebro()
    cerebro.broker.setcash(10000.0)
    data_feed = bt.feeds.PandasData(dataname=flat_df)
    cerebro.adddata(data_feed)
    cerebro.addstrategy(SMAGoldenCross)
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')

    results = cerebro.run()
    strategy_instance = results[0]

    trade_analyzer = strategy_instance.analyzers.trades.get_analysis()
    assert trade_analyzer.total.total == 0


def test_ema_golden_cross_strategy_with_specific_parameters(create_cerebro_and_run):
    """
    Test EMA Golden Cross strategy with specific parameters.
    """
    strategy_instance = create_cerebro_and_run(EMAGoldenCross, fast=5, slow=20)
    assert strategy_instance is not None

def test_macd_strategy_runs(create_cerebro_and_run):
    """
    Test MACD strategy for basic execution.
    """
    strategy_instance = create_cerebro_and_run(MACDStrategy)
    assert strategy_instance is not None

def test_rsi_strategy_runs(create_cerebro_and_run):
    """
    Test RSI strategy for basic execution.
    """
    strategy_instance = create_cerebro_and_run(RSIStrategy)
    assert strategy_instance is not None
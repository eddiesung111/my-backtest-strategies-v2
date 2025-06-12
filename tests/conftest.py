# tests/conftest.py
import pytest
import pandas as pd
import backtrader as bt
from datetime import datetime, timedelta

@pytest.fixture
def sample_data():
    num_days = 100
    start_date = datetime(2023, 1, 1)
    data = []
    prices = []
    for i in range(num_days):
        if i % 10 == 0:
            prices.append(100 + i * 0.5 - 5)
        else:
            prices.append(100 + i * 0.5)

    for i in range(num_days):
        dt = start_date + timedelta(days=i)
        open_price = prices[i]
        close_price = prices[i] * (1 + 0.001 * (1 if i % 2 == 0 else -1))
        high_price = max(open_price, close_price) + 0.5
        low_price = min(open_price, close_price) - 0.5
        volume = 1000 + i * 10
        data.append([dt, open_price, high_price, low_price, close_price, volume])

    df = pd.DataFrame(data, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    df.set_index('datetime', inplace=True)
    return df

@pytest.fixture
def create_cerebro_and_run(sample_data):
    def _run_cerebro_with_strategy(strategy_class, cash=10000.0, **strategy_params):
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(cash)
        data_feed = bt.feeds.PandasData(
            dataname=sample_data,
            open='open',
            high='high',
            low='low',
            close='close',
            volume='volume',
            openinterest=-1
        )

        cerebro.adddata(data_feed)
        cerebro.addstrategy(strategy_class, **strategy_params)
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
        cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')
        cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')

        results = cerebro.run()
        return results[0]

    return _run_cerebro_with_strategy
import os, sys, argparse
import backtrader as bt
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from strategies.SMAGoldenCross import SMAGoldenCross
from strategies.BuyHold import BuyHold
from strategies.MACD_Strategy import MACDStrategy
from strategies.RSI_Strategy import RSIStrategy
from strategies.EMAGoldenCross import EMAGoldenCross

strategies = {
    "5": SMAGoldenCross,
    "1": BuyHold,
    "3": MACDStrategy,
    "4": RSIStrategy,
    "2": EMAGoldenCross
}

parser = argparse.ArgumentParser()
parser.add_argument("strategies", help = "which strategy to run", type = str)
args = parser.parse_args()

if not args.strategies in strategies:
    print("invalid strategy, must be one of {}".format(strategies.keys()))
    sys.exit()


symbol = "TSM"  # Change to any stock ticker
start_date = "2015-01-01"
end_date = "2019-12-31"

# Fetch data from Yahoo Finance
df = yf.download(symbol, start=start_date, end=end_date)

# Rename columns to match Backtrader's expected format
df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
df.columns = ['open', 'high', 'low', 'close', 'volume']
data = bt.feeds.PandasData(dataname=df)

cerebro = bt.Cerebro()
cerebro.broker.setcash(10000.0)
cerebro.adddata(data)
cerebro.addanalyzer(bt.analyzers.Returns, _name = 'returns')
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name = 'sharpe_ratio')
cerebro.addanalyzer(bt.analyzers.DrawDown, _name = 'drawdown')
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name = 'trade_analyzer')

cerebro.addstrategy(strategies[args.strategies])
# Run your strategy
results = cerebro.run()
strategy_instance = results[0]  # Access the first (and only) strategy instance

# Extract some performance metrics:
returns_analysis = strategy_instance.analyzers.returns.get_analysis()
sharpe_analysis = strategy_instance.analyzers.sharpe_ratio.get_analysis()
drawdown_analysis = strategy_instance.analyzers.drawdown.get_analysis()
trade_analysis = strategy_instance.analyzers.trade_analyzer.get_analysis()
perf_metrics = {
    'Total Return': returns_analysis.get('rtot'),
    'Normalized Return': returns_analysis.get('rnorm'),
    'Sharpe Ratio': sharpe_analysis.get('sharperatio'),
    'Max Drawdown': drawdown_analysis.get('max', {}).get('drawdown'),
    'Total Trades': trade_analysis.get('total').get('total', 0),
    'Win rate': trade_analysis.get('won').get('total', 0) / trade_analysis.get('total').get('total', 0)
}
print()
for key, value in perf_metrics.items():
    print(f"{key}: {value}")

cerebro.plot()
#!/usr/bin/env python3
import sys
import argparse
import backtrader as bt
import yfinance as yf
import matplotlib.pyplot as plt # Added for plotting

# Strategy imports - IMPORTANT: USE ABSOLUTE IMPORTS
from src.backtest_strategies.strategies.buy_hold import BuyHold
from src.backtest_strategies.strategies.sma_golden_cross import SMAGoldenCross
from src.backtest_strategies.strategies.ema_golden_cross import EMAGoldenCross
from src.backtest_strategies.strategies.macd_strategy import MACDStrategy
from src.backtest_strategies.strategies.rsi_strategy import RSIStrategy

STRATEGIES = { # Changed variable name to avoid conflict with `strategies` dictionary
    "BuyHold": BuyHold,
    "EMAGoldenCross": EMAGoldenCross,
    "MACDStrategy": MACDStrategy,
    "RSIStrategy": RSIStrategy,
    "SMAGoldenCros": SMAGoldenCross,
}

# IMPORTANT: Wrap your main logic in a function
def main(argv=None):
    argv = argv or sys.argv[1:]
    parser = argparse.ArgumentParser(
        prog="backtest-strategies",
        description="Run a BackTrader strategy and show performance metrics and plot."
    )
    parser.add_argument("strategy", choices=STRATEGIES.keys(), help="Strategy key") # Changed argument name
    parser.add_argument("--symbol", default="TSM")
    parser.add_argument("--start", default="2015-01-01")
    parser.add_argument("--end", default="2019-12-31")
    args = parser.parse_args(argv)

    # Download data
    df = yf.download(args.symbol, start=args.start, end=args.end)
    df = df[['Open','High','Low','Close','Volume']]
    df.columns = ['open','high','low','close','volume']

    # Cerebro setup
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(10000.0)
    data = bt.feeds.PandasData(dataname=df)
    cerebro.adddata(data)
    cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')

    # Run strategy
    cerebro.addstrategy(STRATEGIES[args.strategy]) # Use STRATEGIES and args.strategy
    results = cerebro.run()
    strat = results[0]

    # Extract metrics
    returns = strat.analyzers.getbyname('returns').get_analysis()
    rnorm = returns.get('rnorm')
    sharpe = strat.analyzers.getbyname('sharpe').get_analysis().get('sharperatio')
    maxdd = strat.analyzers.getbyname('drawdown').get_analysis().get('max',{}).get('drawdown')
    total_trades = strat.analyzers.getbyname('trades').get_analysis().get('total',{}).get('total',0)

    # You had different print statements and analysis. I'm using the ones from the first run.py you shared, as they seem more complete.
    print(f"Total Return: {returns.get('rtot')}")
    print(f"Normalized Return: {rnorm}")
    print(f"Sharpe Ratio: {sharpe}")
    print(f"Max Drawdown: {maxdd}")
    print(f"Total Trades: {total_trades}")

    # Plotting (add the save-to-file logic from previous suggestion if interactive still fails)
    try:
        cerebro.plot()
    except Exception as e:
        print(f"Interactive plot failed: {e}. Attempting to save plot to file.")
        fig = cerebro.plot(style='candlestick')[0][0]
        fig.savefig('backtest_results.png', dpi=300)
        print("Plot saved to backtest_results.png")

    return 0

if __name__ == "__main__":
    sys.exit(main())
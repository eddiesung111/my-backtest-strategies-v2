# src/backtest_strategies/strategies/macd_strategy.py
import backtrader as bt

class MACDStrategy(bt.Strategy):
    # Your strategy's parameters. Keep these as they are.
    params = (('fast_period', 12),
              ('slow_period', 26),
              ('signal_period', 9),)

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None

        # Correct way to instantiate MACD indicator by mapping your strategy's
        # parameter names to the MACD indicator's expected parameter names.
        self.macd = bt.indicators.MACD(self.dataclose,
                                       period_me1=self.p.fast_period,        # Map fast_period to period_me1
                                       period_me2=self.p.slow_period,        # Map slow_period to period_me2
                                       period_signal=self.p.signal_period)    # Map signal_period to period_signal

        # This line remains correct as it uses the output lines of the MACD indicator
        self.crossover = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)

    def next(self):
        if self.order:
            return

        if not self.position:
            if self.crossover > 0:
                self.order = self.buy()
        else:
            if self.crossover < 0:
                self.order = self.close()

    def notify_order(self, order):
        if order.status in [order.Completed, order.Canceled, order.Rejected]:
            self.order = None
import backtrader as bt

class EMAGoldenCross(bt.Strategy):
    params = (
        ('fast', 12),
        ('slow', 26)
    )

    def __init__(self):
        self.last_day = self.data.datetime.date(-1)
        self.fast_moving_average = bt.indicators.EMA(
            self.data.close, period = self.params.fast, plotname = '50 days moving average'
        )
        self.slow_moving_average = bt.indicators.EMA(
            self.data.close, period = self.params.slow, plotname = '200 days moving average'
        )
        self.crossover = bt.indicators.CrossOver(self.fast_moving_average, self.slow_moving_average, plot = False)
    
    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.size = self.broker.cash / self.data.close
                print("Buy {} shares at {} on {}".format(self.size, self.data.close[0], self.data.datetime.date(0)))
                self.buy(size = self.size)

        if self.position:
            if self.crossover < 0:
                print("Sell {} shares at {} on {}".format(self.size, self.data.close[0], self.data.datetime.date(0)))
                self.close()
        if self.position and self.last_day == self.data.datetime.date(0):
            self.close()
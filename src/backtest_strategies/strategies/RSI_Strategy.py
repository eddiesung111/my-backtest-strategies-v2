import backtrader as bt

class RSIStrategy(bt.Strategy):
    params = (
        ('rsi_period', 14),
        ('rsi_overbought', 70),
        ('rsi_oversold', 30),
    )

    def __init__(self):
        self.rsi = bt.indicators.RelativeStrengthIndex(
            self.data.close, period=self.params.rsi_period
        )
        self.rsi_overbought = self.params.rsi_overbought
        self.rsi_oversold = self.params.rsi_oversold
        self.last_day = self.data.datetime.date(-1)

    def log(self, action, shares, price):
        date = self.datas[0].datetime.date(0)
        print(f"{date} - {action} {shares} shares at {price:.2f}")

    def next(self):
        if self.position:
            if self.position.size > 0 and self.rsi[0] > self.rsi_overbought:
                self.log("TP", self.position.size, self.data.close[0])
                self.close()
            
            if self.position.size < 0 and self.rsi[0] < self.rsi_oversold:
                self.log("TP", self.position.size, self.data.close[0])
                self.close()

        if not self.position:
            if self.rsi[0] < self.rsi_oversold:
                size = self.broker.cash / self.data.close[0]
                self.log("Buy", size, self.data.close[0])
                self.buy(size=size)

            if self.rsi[0] > self.rsi_overbought:
                size = self.broker.cash / self.data.close[0]
                self.log("Sell", size, self.data.close[0])
                self.sell(size=size)

        if self.position and self.last_day == self.data.datetime.date(0):
            self.close()
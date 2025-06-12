import backtrader as bt
import os

class MACDStrategy(bt.Strategy):
    def __init__(self):
        self.last_day = self.data.datetime.date(-1)
        self.macd = bt.indicators.MACD(self.data.close, plot = False)


            
    def log(self, action, shares, price):
        date = self.datas[0].datetime.date(0)
        print(f"{date} - {action} {shares} shares at {price:.2f}")
    
    def next(self):
        print(self.macd.signal)
        size = self.broker.cash / self.data.close[0]
        if not self.position:
            if self.crossover > 0:
                self.log("Buy", size, self.data.close[0])
                self.buy(size = size)
            elif self.crossover < 0:
                self.log("Sell",size, self.data.close[0])
                self.sell(size = size)
        else:
            if self.crossover < 0:
                self.log("TP",size, self.data.close[0])
                self.close()
            elif self.crossover > 0:
                self.log("TP",size, self.data.close[0])
                self.close()
        if self.position and self.last_day == self.data.datetime.date(0):
            self.close()
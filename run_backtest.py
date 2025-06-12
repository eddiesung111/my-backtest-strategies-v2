# run_backtest.py

import backtrader as bt
import pandas as pd
from datetime import datetime, timedelta
import os
import sys # For redirecting stdout to a log file

# --- 0. Setup Output Directory Structure ---
OUTPUT_DIR = 'outputs'
REPORTS_DIR = os.path.join(OUTPUT_DIR, 'reports')
TRADES_DIR = os.path.join(OUTPUT_DIR, 'trades') # Will explain how to populate this
CHARTS_DIR = os.path.join(OUTPUT_DIR, 'charts')
LOGS_DIR = os.path.join(OUTPUT_DIR, 'logs')

# Create directories if they don't exist
for d in [REPORTS_DIR, TRADES_DIR, CHARTS_DIR, LOGS_DIR]:
    os.makedirs(d, exist_ok=True)

# --- 1. Helper: Data Generation (similar to your fixture for standalone use) ---
def get_sample_data(num_days=100):
    start_date = datetime(2023, 1, 1)
    data = []
    prices = []
    for i in range(num_days):
        # Generate some price fluctuation
        prices.append(100 + i * 0.5 + (0.5 * (i % 5 - 2)))

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

# --- 2. Helper: Custom Observer for Detailed Trade Logging ---
# Backtrader's TradeAnalyzer gives summary stats. For a list of individual trades,
# a custom observer is often the cleanest way.
class TradeLogger(bt.Observer):
    # CRUCIAL FIX: Explicitly declare no lines for this observer
    lines = () # <--- ADD THIS LINE!

    def __init__(self):
        self.trades = []

    def notify_trade(self, trade):
        if trade.isclosed: # Only log closed trades
            self.trades.append({
                'Ref': trade.ref,
                'DateOpen': bt.num2date(trade.dtopen).isoformat(),
                'PriceOpen': trade.priceopen,
                'DateClose': bt.num2date(trade.dtclose).isoformat(),
                'PriceClose': trade.priceclose,
                'Status': 'Closed',
                'Size': trade.size,
                'Value': trade.value,
                'Commission': trade.commission,
                'Pnl': trade.pnl,
                'PnlPct': (trade.pnlcomm / trade.value * 100) if trade.value else 0,
                'BarsHeld': trade.barlen,
            })
    def get_trades_df(self):
        return pd.DataFrame(self.trades)

# --- 3. Main Backtesting and Output Generation Function ---
def run_backtest_and_generate_outputs(strategy_class, strategy_params={}, data_df=None, strategy_name="UnnamedStrategy"):
    print(f"\n--- Running Backtest for {strategy_name} ---")

    cerebro = bt.Cerebro()
    cerebro.broker.setcash(100000.0) # Starting cash
    cerebro.broker.setcommission(commission=0.001) # 0.1% commission

    if data_df is None:
        data_df = get_sample_data() # Use default sample data if not provided

    data_feed = bt.feeds.PandasData(
        dataname=data_df,
        open='open',
        high='high',
        low='low',
        close='close',
        volume='volume',
        openinterest=-1
    )
    cerebro.adddata(data_feed)
    cerebro.addstrategy(strategy_class, **strategy_params)

    # Add Analyzers (for summary reports)
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
    cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    cerebro.addanalyzer(bt.analyzers.SQN, _name='sqn')

    # Add Custom Observer for detailed trades
    cerebro.addobserver(TradeLogger) # This collects individual trade details

    # --- Setup Logging to File ---
    log_file_path = os.path.join(LOGS_DIR, f"{strategy_name}_run.log")
    # Redirect stdout to the log file
    original_stdout = sys.stdout # Save original stdout
    sys.stdout = open(log_file_path, 'w')
    print(f"--- Backtest Log for {strategy_name} ---")
    print(f"Start Time: {datetime.now()}")

    # --- Run Backtest ---
    print("\nRunning backtest...")
    results = cerebro.run()
    strategy_instance = results[0]
    print("Backtest finished.")
    print(f"End Time: {datetime.now()}")
    sys.stdout.close() # Close the log file
    sys.stdout = original_stdout # Restore original stdout

    # --- Generate Reports (Summary Metrics) ---
    print(f"Generating summary report for {strategy_name}...")
    trades_analysis = strategy_instance.analyzers.trades.get_analysis()
    returns_analysis = strategy_instance.analyzers.returns.get_analysis()
    sharpe_analysis = strategy_instance.analyzers.sharpe.get_analysis()
    drawdown_analysis = strategy_instance.analyzers.drawdown.get_analysis()
    sqn_analysis = strategy_instance.analyzers.sqn.get_analysis()

    summary_data = {
        'Strategy': strategy_name,
        'Total Trades': trades_analysis.total.total,
        'Winning Trades': trades_analysis.won.total,
        'Losing Trades': trades_analysis.lost.total,
        'Win Rate (%)': (trades_analysis.won.total / trades_analysis.total.total * 100) if trades_analysis.total.total > 0 else 0,
        'Gross Profit': trades_analysis.won.pnl.gross,
        'Gross Loss': trades_analysis.lost.pnl.gross,
        'Net Profit': trades_analysis.pnl.net,
        'Total Return (%)': returns_analysis['rnorm100'] if 'rnorm100' in returns_analysis else None, # Normalized return in percentage
        'Annualized Return (%)': returns_analysis['rnorm'] * 100 if 'rnorm' in returns_analysis else None,
        'Sharpe Ratio': sharpe_analysis['sharperatio'] if 'sharperatio' in sharpe_analysis else None,
        'Max Drawdown (%)': drawdown_analysis.max.drawdown if 'max' in drawdown_analysis else None,
        'SQN': sqn_analysis.sqn if 'sqn' in sqn_analysis else None,
        'Final Value': cerebro.broker.getvalue()
    }
    summary_df = pd.DataFrame([summary_data]).set_index('Strategy')
    summary_file_path = os.path.join(REPORTS_DIR, f"{strategy_name}_summary.csv")
    summary_df.to_csv(summary_file_path)
    print(f"Summary report saved to {summary_file_path}")

    # --- Generate Detailed Trades List ---
    print(f"Generating detailed trades report for {strategy_name}...")
    # Access the custom TradeLogger observer's get_trades_df method
    # It will be in strategy_instance.observers[0] if it's the first observer added
    # Or by name if you added it like cerebro.addobserver(TradeLogger, _name='my_trade_logger')
    trade_logger_instance = None
    for obs in strategy_instance.observers:
        if isinstance(obs, TradeLogger):
            trade_logger_instance = obs
            break

    if trade_logger_instance:
        detailed_trades_df = trade_logger_instance.get_trades_df()
        trades_file_path = os.path.join(TRADES_DIR, f"{strategy_name}_trades.csv")
        detailed_trades_df.to_csv(trades_file_path, index=False)
        print(f"Detailed trades saved to {trades_file_path}")
    else:
        print("TradeLogger observer not found. Detailed trades not generated.")


    # --- Generate Charts ---
    print(f"Generating chart for {strategy_name}...")
    chart_file_path = os.path.join(CHARTS_DIR, f"{strategy_name}_chart.png")
    try:
        # cerebro.plot() can save to a file. iplot=False prevents interactive window.
        # numfigs=1 ensures it only saves the first figure if multiple are generated.
        cerebro.plot(style='candlestick', barupcolor='green', bardowncolor='red',
                     savefig=True, figfilename=chart_file_path,
                     numfigs=1, iplot=False)
        print(f"Chart saved to {chart_file_path}")
    except Exception as e:
        print(f"Error generating chart: {e}. Make sure you have matplotlib installed (`pip install matplotlib`) and a backend configured if running headless.")


# --- Example Usage (when run directly) ---
if __name__ == "__main__":
    # Import your strategies
    from src.backtest_strategies.strategies.buy_hold import BuyHold
    from src.backtest_strategies.strategies.ema_golden_cross import EMAGoldenCross
    from src.backtest_strategies.strategies.sma_golden_cross import SMAGoldenCross

    print("Starting backtesting and output generation process...")

    # Run BuyHold strategy
    run_backtest_and_generate_outputs(BuyHold, strategy_name="BuyHold_Strategy")

    # Run EMA Golden Cross strategy with specific parameters
    run_backtest_and_generate_outputs(EMAGoldenCross, strategy_params={'fast': 5, 'slow': 20}, strategy_name="EMA_Golden_Cross_Strategy")

    # Run SMA Golden Cross strategy (using standard parameters for sample data)
    run_backtest_and_generate_outputs(SMAGoldenCross, strategy_params={'fast': 10, 'slow': 20}, strategy_name="SMA_Golden_Cross_Strategy")

    print("\nAll backtests completed and outputs generated!")
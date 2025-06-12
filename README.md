My Backtest Strategies v2: A Backtrader Framework
A robust and extensible framework for developing, testing, and analyzing quantitative trading strategies using the Backtrader library. This project provides a structured environment for quickly implementing new strategies, running comprehensive backtests, and generating detailed performance reports and visualizations.

✨ Features
Modular Strategy Development: Easily define and integrate new trading strategies.

Automated Backtesting: Run multiple strategies against historical data with configurable parameters.

Comprehensive Performance Analysis: Utilize Backtrader's built-in analyzers for key metrics (Returns, Sharpe Ratio, Drawdown, SQN, etc.).

Detailed Trade Logging: Custom observer to capture and export individual trade details (entry/exit dates, prices, PnL, etc.).

Automated Chart Generation: Visualize strategy performance and trade execution directly from backtest results.

Structured Output Management: Organize all reports, trade logs, charts, and backtest logs into a dedicated outputs/ directory.

pytest-Based Testing: Ensure the reliability and correctness of your strategies and core components.

📂 Project Structure
.
├── docs/                               # Comprehensive documentation files
│   ├── backtrader_setup.md             # Guide to setting up Backtrader environment
│   ├── strategies.md                   # Detailed descriptions of all trading strategies
│   └── usage.md                        # General usage guide for the framework (placeholder)
├── src/                                # Source code for strategies and core logic
│   └── backtest_strategies/
│       ├── strategies/                 # Individual trading strategy implementations
│       │   ├── buy_hold.py
│       │   ├── ema_golden_cross.py
│       │   ├── macd_strategy.py
│       │   ├── rsi_strategy.py
│       │   └── sma_golden_cross.py
│       ├── __init__.py
│       ├── __main__.py
│       └── run.py                      # Main script for running individual strategies (as per initial setup)
├── tests/                              # Unit and integration tests for strategies and components
│   ├── conftest.py
│   ├── __init__.py
│   └── test_strategies.py
├── outputs/                            # Directory for generated backtest results (reports, charts, logs)
├── .gitignore                          # Specifies intentionally untracked files to ignore
├── LICENSE                             # Project licensing information
├── README.md                           # This file
└── requirements.txt                    # Python dependencies for the project

🚀 Getting Started
Follow these steps to set up the project and run your first backtest.

Prerequisites
Python: Recommended versions are Python 3.10, 3.11, or 3.12. While Python 3.13 may be used, backtrader and its dependencies might exhibit compatibility issues.

Git: For cloning the repository.

Installation
Clone the repository:

git clone https://github.com/eddiesung111/my-backtest-strategies-v2.git
cd my-backtest-strategies-v2

(Remember to replace your_username with your actual GitHub username or the correct repository URL.)

Create and activate a virtual environment:

python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# .\.venv\Scripts\Activate.ps1  # On Windows PowerShell
# .venv\Scripts\activate.bat   # On Windows Command Prompt

Install project dependencies:

pip install -r requirements.txt

This will install backtrader, pandas, matplotlib, and any other required libraries.

📈 How to Run Backtests
The run_backtest.py script is the main entry point for executing strategies and generating backtest outputs.

To run all configured backtests (e.g., Buy & Hold, EMA Golden Cross, etc.):

python3 run_backtest.py

The script will automatically generate performance summaries, detailed trade lists, and charts, saving them into the outputs/ directory. You can modify run_backtest.py to select specific strategies or adjust their parameters.

📊 Understanding the Outputs
All backtest results are organized in the outputs/ directory:

outputs/reports/: Contains CSV files with summary performance metrics for each strategy.

outputs/trades/: Contains CSV files with detailed logs of individual trades executed by each strategy.

outputs/charts/: Contains PNG image files of the equity curve and trade plots for each strategy.

outputs/logs/: Contains text log files capturing the console output during each backtest run.

🧠 Strategies Implemented
This framework includes the following trading strategies:

BuyHold: A baseline strategy that simply buys and holds the asset for the entire backtest period.

SMAGoldenCross: A trend-following strategy based on the crossover of two Simple Moving Averages.

EMAGoldenCross: A trend-following strategy based on the crossover of two Exponential Moving Averages.

MACDStrategy: Utilizes the Moving Average Convergence Divergence indicator for momentum and trend signals.

RSIStrategy: Employs the Relative Strength Index to identify overbought/oversold conditions and potential reversals.

For detailed descriptions, logic, and parameters of each strategy, refer to the Strategies documentation.

✅ Testing
The project includes a test suite to ensure the correctness and reliability of the strategies and core components.

To run all tests:

pytest

📚 Documentation
For more in-depth information, please refer to the docs/ directory:

Backtrader Setup: Detailed instructions for setting up your development environment.

Strategies: Comprehensive details on each implemented trading strategy.

Usage: A guide on how to use various parts of the framework beyond basic backtesting. (Placeholder)

🤝 Contributing
Contributions are welcome! Please see the relevant documentation in the docs/ directory for guidelines on how to contribute.

📄 License
This project is licensed under the MIT License.
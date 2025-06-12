# My Backtest Strategies v2: A Backtrader Framework

A robust and extensible framework for developing, testing, and analyzing quantitative trading strategies using the Backtrader library. This project provides a structured environment for quickly implementing new strategies, running comprehensive backtests, and generating detailed performance reports and visualizations.

## ✨ Features

* **Modular Strategy Development:** Easily define and integrate new trading strategies.
* **Automated Backtesting:** Run multiple strategies against historical data with configurable parameters.
* **Comprehensive Performance Analysis:** Utilize Backtrader's built-in analyzers for key metrics (Returns, Sharpe Ratio, Drawdown, SQN, etc.).
* **Detailed Trade Logging:** Custom observer to capture and export individual trade details (entry/exit dates, prices, PnL, etc.).
* **Automated Chart Generation:** Visualize strategy performance and trade execution directly from backtest results.
* **Structured Output Management:** Organize all reports, trade logs, charts, and backtest logs into a dedicated `outputs/` directory.
* **`pytest`-Based Testing:** Ensure the reliability and correctness of your strategies and core components.

## 📂 Project Structure

```

.
├── docs/                               \# Comprehensive documentation files
│   ├── backtrader\_setup.md             \# Guide to setting up Backtrader environment
│   └── strategies.md                   \# Detailed descriptions of all trading strategies
├── src/                                \# Source code for strategies and core logic
│   └── backtest\_strategies/
│       ├── strategies/                 \# Individual trading strategy implementations
│       └── **init**.py
│       └── **main**.py
│       └── run.py                      \# (If this is used for something separate)
├── tests/                              \# Unit and integration tests for strategies and components
├── outputs/                            \# Directory for generated backtest results (reports, charts, logs)
├── .gitignore                          \# Specifies intentionally untracked files to ignore
├── LICENSE
├── README.md          
└── requirements.txt       
 

````

## 🚀 Getting Started

Follow these steps to set up the project and run your first backtest.

### Prerequisites

* **Python:** Recommended versions are **Python 3.10, 3.11, or 3.12**. While Python 3.13 may be used, `backtrader` and its dependencies might exhibit compatibility issues.
* **Git:** For cloning the repository.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/eddiesung111/my-backtest-strategies-v2.git](https://github.com/eddiesung111/my-backtest-strategies-v2.git)
    cd my-backtest-strategies-v2
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On macOS/Linux
    # .\.venv\Scripts\Activate.ps1  # On Windows PowerShell
    # .venv\Scripts\activate.bat   # On Windows Command Prompt
    ```

3.  **Install project dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    This will install `backtrader`, `pandas`, `matplotlib`, and any other required libraries.

## 🧠 Strategies Implemented

This framework includes the following trading strategies:

  * **BuyHold:** A baseline strategy that simply buys and holds the asset for the entire backtest period.
  * **SMAGoldenCross:** A trend-following strategy based on the crossover of two Simple Moving Averages.
  * **EMAGoldenCross:** A trend-following strategy based on the crossover of two Exponential Moving Averages.
  * **MACDStrategy:** Utilizes the Moving Average Convergence Divergence indicator for momentum and trend signals.
  * **RSIStrategy:** Employs the Relative Strength Index to identify overbought/oversold conditions and potential reversals.

For detailed descriptions, logic, and parameters of each strategy, refer to the [Strategies documentation](https://www.google.com/search?q=docs/strategies.md).

## Run the progrma
You can simply use the following command to run the program.
```bash
python3 src/backtest_strategies/run.py [Strategies]
```
Strategies could be:
* BuyHold,
* EMAGoldenCross
* MACDStrategy
* RSIStrategy
* SMAGoldenCross

## ✅ Testing

The project includes a test suite to ensure the correctness and reliability of the strategies and core components.

To run all tests:

```bash
pytest
```

## 📚 Documentation

For more in-depth information, please refer to the `docs/` directory:

  * [**Backtrader Setup**](https://www.google.com/search?q=docs/backtrader_setup.md): Detailed instructions for setting up your development environment.
  * [**Strategies**](https://www.google.com/search?q=docs/strategies.md): Comprehensive details on each implemented trading strategy.
  * [**Usage**](https://www.google.com/search?q=docs/usage.md): A guide on how to use various parts of the framework beyond basic backtesting.

## 🤝 Contributing

Contributions are welcome\! Please see the relevant documentation in the `docs/` directory for guidelines on how to contribute.

## 📄 License

This project is licensed under the [MIT License](https://www.google.com/search?q=LICENSE).

```
```
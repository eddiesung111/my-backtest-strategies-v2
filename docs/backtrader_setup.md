# Backtrader Setup and Environment

This guide will walk you through setting up your development environment to run backtests with `my-backtest-strategies-v2`, focusing on common practices and troubleshooting steps for Backtrader.

## 1. Introduction to Backtrader

[Backtrader](https://www.backtrader.com/) is a powerful, flexible, and feature-rich Python framework for backtesting trading strategies. It provides tools for data feeding, strategy execution, performance analysis, and visual charting.

## 2. Prerequisites

Before you begin, ensure you have the following installed on your system:

* **Python:** Recommended versions are **Python 3.10, 3.11, or 3.12**. While Python 3.13 might work in some cases, `backtrader` and its dependencies may exhibit compatibility issues or unexpected behavior with very new Python releases due to internal changes in the interpreter.
* **Git:** For cloning the project repository.

## 3. Step-by-Step Setup

Follow these steps to set up your project environment:

### Step 3.1: Clone the Repository

Open your terminal or command prompt and run:

```bash
git clone https://github.com/eddiesung111/my-backtest-strategies-v2.git
cd my-backtest-strategies-v2
```
### Step 3.2: Create a Virtual Environment
It is highly recommended to use a virtual environment to manage project dependencies. This isolates the project's libraries from your system's global Python installation, preventing conflicts.
```bash
# Ensure you are in the project root directory (my-backtest-strategies-v2)
python3 -m venv .venv
```

This command creates a new directory named .venv (or whatever you choose) in your project folder, which will contain a local copy of the Python interpreter and pip.

### Step 3.3: Activate the Virtual Environment
Before installing any packages or running scripts, you must activate the virtual environment.

On macOS / Linux:
```bash
source .venv/bin/activate
```
On Windows (PowerShell):
```powershell
.venv\Scripts\Activate.ps1
```

On Windows (Command Prompt):
```DOS
.venv\Scripts\activate.bat
```
You will know the virtual environment is active when your terminal prompt changes to include (.venv) (or similar) at the beginning.

### Step 3.4: Install Project Dependencies
Once your virtual environment is active, install backtrader, pandas, and matplotlib:

```bash
pip install backtrader pandas matplotlib
```

backtrader: The core backtesting framework.
pandas: Used for data manipulation, especially when loading data into Backtrader.
matplotlib: Used by Backtrader for generating charts of your backtest results.
(Optional: Create requirements.txt)
After successfully installing all dependencies, you can create a requirements.txt file to easily manage and share your project's dependencies:

```bash
pip freeze > requirements.txt
```
Then, others (or you in the future) can install all dependencies with a single command: pip install -r requirements.txt

Step 3.5: Deactivate the Virtual Environment
When you are done working on the project, you can deactivate the virtual environment:

```bash
deactivate
```
Your terminal prompt will return to its normal state.
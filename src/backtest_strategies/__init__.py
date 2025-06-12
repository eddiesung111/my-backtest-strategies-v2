"""
backtest_strategies
~~~~~~~~~~~~~~~~~~~~
A small framework for running BackTrader strategies.
"""

__version__ = "0.1.0"
__all__ = ["main", "__version__"]

from .run import main  # exposes main() at package level
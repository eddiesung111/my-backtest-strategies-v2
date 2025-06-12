#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="backtest_strategies",
    version="0.1.0",
    description="A small framework for running and comparing BackTrader strategies",
    author="Your Name",
    author_email="you@example.com",
    url="https://github.com/yourusername/my-backtest-strategies-v2",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "backtrader>=1.9.74.123",
        "yfinance>=0.2.14",
        "pandas>=1.5.0",
        "matplotlib>=3.6.0",
    ],
    entry_points={
        'console_scripts': [
            'backtest-strategies=backtest_strategies.run:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
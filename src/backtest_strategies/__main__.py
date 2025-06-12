# This file allows `python -m backtest_strategies` to work.

import sys
from .run import main

if __name__ == "__main__":
    # Call your main() function with CLI args and use its return code
    sys.exit(main())

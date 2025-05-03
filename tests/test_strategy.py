import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.strategies.futures_strategy import FuturesStrategy

def test_strategy():
    config = {
        'sma_short_period': 9,
        'sma_long_period': 21,
        'rsi_period': 14,
        'macd_fast': 12,
        'macd_slow': 26,
        'macd_signal': 9,
        'atr_period': 14
    }
    strategy = FuturesStrategy(config)
    assert strategy is not None

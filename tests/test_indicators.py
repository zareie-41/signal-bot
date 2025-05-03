import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.indicators.sma import calculate_sma

def test_sma():
    data = [100, 101, 102, 103, 104, 105]
    sma = calculate_sma(data, 3)
    assert abs(sma - 104) < 0.01

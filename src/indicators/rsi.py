import pandas as pd
import pandas_ta as ta

def calculate_rsi(data, period):
    return ta.rsi(pd.Series(data), length=period).iloc[-1]

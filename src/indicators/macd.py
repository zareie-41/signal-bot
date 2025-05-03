import pandas as pd
import pandas_ta as ta

def calculate_macd(data, fast_period, slow_period, signal_period):
    macd = ta.macd(pd.Series(data), fast=fast_period, slow=slow_period, signal=signal_period)
    macd_value = macd[f'MACD_{fast_period}_{slow_period}_{signal_period}'].iloc[-1]
    signal_value = macd[f'MACDs_{fast_period}_{slow_period}_{signal_period}'].iloc[-1]
    status = "Bullish" if macd_value > signal_value else "Bearish"
    return macd_value, signal_value, status

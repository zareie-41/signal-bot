import pandas as pd
import pandas_ta as ta

def calculate_sma(data, period):
    return ta.sma(pd.Series(data), length=period).iloc[-1]

def check_sma_crossover(data, short_period, long_period):
    short_sma = calculate_sma(data, short_period)
    long_sma = calculate_sma(data, long_period)
    prev_short_sma = calculate_sma(data[:-1], short_period)
    prev_long_sma = calculate_sma(data[:-1], long_period)

    if short_sma > long_sma and prev_short_sma <= prev_long_sma:
        return "Bullish Crossover"
    elif short_sma < long_sma and prev_short_sma >= prev_long_sma:
        return "Bearish Crossover"
    return "No Crossover"

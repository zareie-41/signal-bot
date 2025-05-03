import pandas as pd
import pandas_ta as ta

def calculate_atr(high, low, close, period):
    df = pd.DataFrame({'high': high, 'low': low, 'close': close})
    return ta.atr(df['high'], df['low'], df['close'], length=period).iloc[-1]

import pandas as pd

def check_volume(data, period=20):
    current_volume = data[-1]
    avg_volume = pd.Series(data).rolling(window=period).mean().iloc[-1]
    return "High" if current_volume > avg_volume else "Low"

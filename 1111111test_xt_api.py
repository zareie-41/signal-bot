import requests

url = "https://api.xt.com/v4/public/kline"
params = {
    "symbol": "BTCUSDT",
    "interval": "15m",
    "limit": 100
}

try:
    response = requests.get(url, params=params)
    response.raise_for_status()
    print(response.json())
except Exception as e:
    print(f"Error: {str(e)}")

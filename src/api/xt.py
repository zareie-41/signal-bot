import requests
import time
from src.utils.logger import setup_logger

class XTAPI:
    def __init__(self, access_key, secret_key, api_url="https://api.coingecko.com/api/v3"):
        self.access_key = access_key
        self.secret_key = secret_key
        self.api_url = api_url
        self.logger = setup_logger()
        self.logger.info("مقداردهی اولیه API برای CoinGecko انجام شد")

    # نگاشت نمادهای معاملاتی به Coin IDs
    COIN_IDS = {
        "BTCUSDT": "bitcoin",
        "ETHUSDT": "ethereum",
        "BNBUSDT": "binancecoin",
        "XRPUSDT": "ripple"
    }

    def get_ohlc_data(self, market, timeframe, retries=3, delay=5):
        coin_id = self.COIN_IDS.get(market, market.lower().replace("usdt", ""))
        url = f"{self.api_url}/coins/{coin_id}/ohlc?vs_currency=usd&days=1"
        for attempt in range(retries):
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                self.logger.info(f"دریافت داده‌های OHLC برای {market}")
                return [
                    {
                        "timestamp": entry[0],
                        "open": float(entry[1]),
                        "high": float(entry[2]),
                        "low": float(entry[3]),
                        "close": float(entry[4]),
                        "volume": 0.0  # CoinGecko حجم ارائه نمی‌دهد
                    } for entry in data[:100]
                ]
            except requests.exceptions.HTTPError as http_err:
                self.logger.error(f"خطای HTTP برای {market}: {str(http_err)}")
                time.sleep(delay)
                continue
            except Exception as e:
                self.logger.error(f"استثنای عمومی برای {market}: {str(e)}")
                return None
        self.logger.error(f"تلاش‌ها برای {market} ناموفق بود پس از {retries} بار")
        return None

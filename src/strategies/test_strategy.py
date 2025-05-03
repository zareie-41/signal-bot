import pandas as pd
from src.utils.logger import setup_logger

class TestStrategy:
    def __init__(self, config):
        self.config = config
        self.logger = setup_logger()
        self.logger.info("مقداردهی اولیه استراتژی تست")

    def generate_signal(self, coin, ohlc_data):
        try:
            if not ohlc_data or len(ohlc_data) < 1:
                self.logger.warning(f"داده‌های ناکافی برای {coin}")
                return None

            df = pd.DataFrame(ohlc_data)
            latest_close = df["close"].iloc[-1]
            self.logger.info(f"مقدار close برای {coin}: {latest_close}")

            # منطق سیگنال ساده برای تست
            signal_type = "BUY" if latest_close > 100 else "SELL"
            volume_status = "N/A"
            sma_status = "N/A"
            macd_status = "N/A"
            rsi_value = 0.0

            # محاسبه حد ضرر و حد سود
            atr = (df["high"] - df["low"]).mean()
            entry_price = float(latest_close)
            stop_loss = float(entry_price - atr * 1.5 if signal_type == "BUY" else entry_price + atr * 1.5)
            take_profit = float(entry_price + atr * 3 if signal_type == "BUY" else entry_price - atr * 3)

            signal = {
                "market": coin,
                "type": signal_type,
                "entry_price": entry_price,
                "stop_loss": stop_loss,
                "take_profit": take_profit,
                "timestamp": int(df["timestamp"].iloc[-1]),
                "sma_status": sma_status,
                "rsi_value": rsi_value,
                "macd_status": macd_status,
                "volume_status": volume_status
            }
            self.logger.info(f"سیگنال تولید شد برای {coin}: {signal}")
            return signal
        except Exception as e:
            self.logger.error(f"خطا در تولید سیگنال برای {coin}: {str(e)}")
            return None

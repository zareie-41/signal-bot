import pandas as pd
from ta.trend import SMAIndicator, MACD
from ta.momentum import RSIIndicator
from src.utils.logger import setup_logger

class FuturesStrategy:
    def __init__(self, config):
        self.config = config
        self.logger = setup_logger()
        self.logger.info("مقداردهی اولیه استراتژی برای CoinGecko")

    def generate_signal(self, coin, ohlc_data):
        try:
            if not ohlc_data or len(ohlc_data) < self.config["rsi_period"]:
                self.logger.warning(f"داده‌های ناکافی برای {coin}")
                return None

            df = pd.DataFrame(ohlc_data)
            latest_close = df["close"].iloc[-1]
            self.logger.info(f"مقدار close برای {coin}: {latest_close}")

            # محاسبه اندیکاتورها
            sma_short = SMAIndicator(df["close"], window=self.config["sma_short_period"]).sma_indicator()
            sma_long = SMAIndicator(df["close"], window=self.config["sma_long_period"]).sma_indicator()
            rsi = RSIIndicator(df["close"], window=self.config["rsi_period"]).rsi()
            macd = MACD(df["close"], window_fast=self.config["macd_fast"], 
                       window_slow=self.config["macd_slow"], window_sign=self.config["macd_signal"])
            
            latest_sma_short = sma_short.iloc[-1]
            latest_sma_long = sma_long.iloc[-1]
            latest_rsi = rsi.iloc[-1]
            macd_line = macd.macd().iloc[-1]
            signal_line = macd.macd_signal().iloc[-1]

            # منطق سیگنال (شل‌شده برای تست)
            sma_status = "Bullish" if latest_sma_short > latest_sma_long else "Bearish"
            macd_status = "Bullish" if macd_line > signal_line else "Bearish"
            volume_status = "N/A"
            signal_type = None

            # شل کردن شرایط برای تولید سیگنال
            if latest_rsi < 45:  # فقط RSI برای خرید
                signal_type = "BUY"
            elif latest_rsi > 55:  # فقط RSI برای فروش
                signal_type = "SELL"

            if signal_type:
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
                    "rsi_value": float(latest_rsi),
                    "macd_status": macd_status,
                    "volume_status": volume_status
                }
                self.logger.info(f"سیگنال تولید شد برای {coin}: {signal}")
                return signal
            else:
                self.logger.info(f"هیچ سیگنالی برای {coin} تولید نشد. RSI: {latest_rsi:.2f}, SMA: {sma_status}, MACD: {macd_status}")
                return None
        except Exception as e:
            self.logger.error(f"خطا در تولید سیگنال برای {coin}: {str(e)}")
            return None

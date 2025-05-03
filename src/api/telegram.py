from telegram import Bot
from telegram.error import TelegramError
from src.utils.logger import setup_logger

class TelegramBot:
    def __init__(self, token, chat_ids):
        self.token = token
        self.chat_ids = chat_ids if isinstance(chat_ids, list) else [chat_ids]
        self.bot = Bot(token=self.token)
        self.logger = setup_logger()
        self.logger.info("مقداردهی اولیه بات تلگرام انجام شد")

    async def send_signal(self, signal):
        try:
            if not signal:
                self.logger.warning("هیچ سیگنالی برای ارسال وجود ندارد")
                return False
            message = (
                f"📊 سیگنال فیوچرز - {signal['timestamp']}\n"
                f"💰 جفت‌ارز: {signal['market']}\n"
                f"📈 نوع: {signal['type']}\n"
                f"🎯 قیمت ورود: {signal['entry_price']:.2f} USDT\n"
                f"🛑 حد ضرر: {signal['stop_loss']:.2f} USDT\n"
                f"🏆 حد سود: {signal['take_profit']:.2f} USDT\n"
                f"📉 اندیکاتورها:\n"
                f"  - SMA: {signal['sma_status']}\n"
                f"  - RSI: {signal['rsi_value']:.2f}\n"
                f"  - MACD: {signal['macd_status']}\n"
                f"  - حجم: {signal['volume_status']}\n"
                f"⚠️ هشدار: مدیریت ریسک را رعایت کنید!"
            )
            for chat_id in self.chat_ids:
                await self.bot.send_message(chat_id=chat_id, text=message)
                self.logger.info(f"پیام به تلگرام ({chat_id}) ارسال شد: {message}")
            return True
        except TelegramError as te:
            self.logger.error(f"خطا در ارسال پیام به تلگرام: {str(te)}")
            return False
        except Exception as e:
            self.logger.error(f"خطای عمومی در ارسال پیام: {str(e)}")
            return False

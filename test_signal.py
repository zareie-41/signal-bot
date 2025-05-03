import asyncio
from src.api.telegram import TelegramBot
from src.utils.logger import setup_logger

async def test_send_signal():
    logger = setup_logger()
    try:
        telegram_bot = TelegramBot(
            token="8078807791:AAFWVqR1cn07kaKYZyYJMfeMIiBFxRK2XIw",
            chat_id="96545679"  # جایگزین با chat_id واقعی
        )
        signal = {
            "coin": "TEST",
            "type": "BUY",
            "price": 100,
            "timestamp": 1234567890
        }
        success = await telegram_bot.send_signal(signal)
        if success:
            logger.info("سیگنال تستی با موفقیت ارسال شد")
        else:
            logger.error("ارسال سیگنال تستی ناموفق بود")
    except Exception as e:
        logger.error(f"خطا در تست ارسال سیگنال: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_send_signal())

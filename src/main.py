import asyncio
import time
from src.api.xt import XTAPI
from src.api.telegram import TelegramBot
from src.strategies.futures_strategy import FuturesStrategy
from src.utils.logger import setup_logger
from src.utils.helpers import load_config, load_coins

async def main():
    logger = setup_logger()
    logger.info("شروع بارگذاری تنظیمات")
    config = load_config()
    logger.info(f"تنظیمات بارگذاری شد: {config}")

    logger.info("مقداردهی اولیه XT API")
    xt_api = XTAPI(config.get("access_key", ""), config.get("secret_key", ""), config["xt_api_url"])

    logger.info("مقداردهی اولیه بات تلگرام")
    chat_ids = [config["telegram_chat_id"], "YOUR_PRIVATE_CHAT_ID"]  # کانال و چت خصوصی
    telegram_bot = TelegramBot(config["telegram_token"], chat_ids)

    logger.info("بارگذاری لیست ارزها")
    coins = load_coins()
    logger.info(f"ارزهای بارگذاری‌شده: {coins}")

    logger.info("مقداردهی اولیه استراتژی برای CoinGecko")
    strategy = FuturesStrategy(config)

    logger.info("بات SIGNAL-BOT با موفقیت شروع شد")
    
    last_signals = {coin: None for coin in coins}  # ذخیره سیگنال‌های قبلی
    
    while True:
        try:
            for coin in coins:
                logger.info(f"پردازش {coin}")
                try:
                    ohlc_data = xt_api.get_ohlc_data(coin, config["timeframe"])
                    if ohlc_data:
                        signal = strategy.generate_signal(coin, ohlc_data)
                        if signal and signal != last_signals[coin]:
                            logger.info(f"ارسال سیگنال برای {coin}: {signal}")
                            success = await telegram_bot.send_signal(signal)
                            if success:
                                logger.info(f"سیگنال برای {coin} ارسال شد: {signal['type']}")
                                last_signals[coin] = signal
                            else:
                                logger.error(f"شکست در ارسال سیگنال برای {coin}")
                    await asyncio.sleep(5)  # تأخیر 5 ثانیه بین ارزها
                except Exception as e:
                    logger.error(f"خطا در پردازش {coin}: {str(e)}")
            logger.info("بررسی بعدی در 30 ثانیه")
            await asyncio.sleep(30)  # تأخیر 30 ثانیه بین چرخه‌ها
        except KeyboardInterrupt:
            logger.info("بات به‌صورت دستی متوقف شد")
            break
        except Exception as e:
            logger.error(f"خطای عمومی: {str(e)}")
            await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())

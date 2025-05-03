import asyncio
from telegram import Bot
from telegram.error import TelegramError

async def test_telegram():
    token = "8078807791:AAFWVqR1cn07kaKYZyYJMfeMIiBFxRK2XIw"
    chat_id = "96545679"  # جایگزین با chat_id واقعی
    try:
        bot = Bot(token=token)
        await bot.send_message(chat_id=chat_id, text="تست بات SIGNAL-BOT")
        print("پیام با موفقیت ارسال شد")
    except TelegramError as e:
        print(f"خطا در ارسال پیام: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_telegram())

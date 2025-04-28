import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN
from handlers import register_all_handlers
from services.database import clear_all_users

# Logging sozlamalari
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

async def main():
    # ✅ Faqat DEBUG rejimda ishlaganda foydalanuvchilarni tozalaydi
    if os.getenv("DEBUG") == "1":
        clear_all_users()

    # 🤖 Botni ishga tushirish
    bot = Bot(token=TOKEN, parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())

    # 📥 Barcha handlerlarni ro‘yxatdan o‘tkazamiz
    register_all_handlers(dp)

    logging.info("🚀 Bot ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

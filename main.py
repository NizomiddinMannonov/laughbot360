# 📁 main.py

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import register_all_handlers
from config import TOKEN
from services.database import clear_all_users

logging.basicConfig(level=logging.INFO)

async def main():
    # ✅ Test rejimida foydalanuvchi maʼlumotlarini tozalash
    clear_all_users()

    bot = Bot(token=TOKEN, parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())

    register_all_handlers(dp)

    logging.info("🚀 Bot ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
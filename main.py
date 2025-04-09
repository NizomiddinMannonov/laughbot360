# main.py

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from os import getenv

# Barcha handlerlarni ro'yxatdan o'tkazish
from handlers import register_all_handlers

load_dotenv()
BOT_TOKEN = getenv("BOT_TOKEN")

async def main():
    logging.basicConfig(level=logging.INFO)
    
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())

    # Barcha handlerlarni ro'yxatdan o'tkazamiz
    register_all_handlers(dp)

    logging.info("🤖 Bot ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

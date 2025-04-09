# main.py

import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from handlers import register_all_handlers

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def main():
    logging.basicConfig(level=logging.INFO)
    
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())

    # Barcha handlerlarni ro'yxatdan o'tkazish
    register_all_handlers(dp)

    logging.info("🤖 Bot ishga tushdi!")
    await dp.start_polling(bot)

# Botni ishlatish shart bilan (RUN_BOT=true bo'lsa)
if __name__ == "__main__":
    if os.getenv("RUN_BOT", "true") == "true":
        asyncio.run(main())
    else:
        print("🚫 Render: RUN_BOT=false — Bot ishga tushmadi")

# main.py
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from os import getenv
from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message()
async def echo_handler(message: Message):
    await message.answer("Salom! Bot ishlayapti 🎉")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

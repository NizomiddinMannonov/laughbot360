# handlers/base.py
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    # Dinamik asosiy menyuga o'tish: foydalanuvchiga qulay variantlarni taklif qilamiz
    text = "👋 Salom! Men Laughbot360 botiman.\n" \
           "Iltimos, menyudan birini tanlang:\n" \
           "1️⃣ AI Savol-Javob\n" \
           "2️⃣ Mem yaratish\n" \
           "3️⃣ Tilni o‘zgartirish (uz/en/ru)"
    await message.answer(text)

@router.message()
async def fallback(message: Message):
    await message.answer("🤖 Men sizning so‘rovingizni tushunmadim. Iltimos, menyuni tanlang.")

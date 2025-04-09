# handlers/base.py

from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🧠 AI Savol-Javob"), KeyboardButton(text="🖼 Mem yaratish")],
            [KeyboardButton(text="🌐 Tilni o‘zgartirish")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Bo‘limlardan birini tanlang..."
    )

    text = (
        "👋 Salom! Men Laughbot360 botiman.\n"
        "Iltimos, menyudan birini tanlang:"
    )
    await message.answer(text, reply_markup=keyboard)

@router.message()
async def fallback(message: Message):
    await message.answer("🤖 Men sizning so‘rovingizni tushunmadim. Iltimos, menyudagi tugmalarni tanlang.")

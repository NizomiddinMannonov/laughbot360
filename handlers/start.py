# handlers/start.py

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from services.database import get_user_language, save_user_language
from localization.texts import texts
from keyboards.reply import get_main_keyboard

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id

    # Yangi foydalanuvchilar uchun default til: inglizcha
    lang = get_user_language(user_id)
    if lang is None:
        lang = "en"
        save_user_language(user_id, lang)

    text = texts[lang]["start"]
    keyboard = get_main_keyboard(lang)

    await message.answer(text, reply_markup=keyboard)

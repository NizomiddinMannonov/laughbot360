# handlers/language.py

from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from services.database import save_user_language

router = Router()

@router.message(F.text == "🌐 Tilni o‘zgartirish")
async def show_language_options(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇺🇿 O‘zbekcha", callback_data="lang:uz")],
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en")]
    ])
    await message.answer("🌐 Iltimos, tilni tanlang:", reply_markup=keyboard)

@router.callback_query(F.data.startswith("lang:"))
async def handle_language_selection(callback: CallbackQuery):
    lang_code = callback.data.split(":")[1]
    save_user_language(callback.from_user.id, lang_code)

    message_map = {
        "uz": "🇺🇿 Til muvaffaqiyatli o‘zgartirildi: O‘zbek tili",
        "ru": "🇷🇺 Язык успешно изменен: Русский",
        "en": "🇬🇧 Language successfully changed: English"

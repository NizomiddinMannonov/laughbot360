from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from services.database import save_user_language, get_user_language
from localization.texts import get_text
from keyboards.reply import get_main_keyboard

router = Router()

# Tillar va matnlari
languages = {
    "en": "English 🇬🇧",
    "uz": "O‘zbek 🇺🇿",
    "ru": "Русский 🇷🇺"
}

# --- 1. Settings menyusi va til tanlash
@router.message(F.text.in_([
    "/settings",
    get_text("change_lang", "en"),
    get_text("change_lang", "uz"),
    get_text("change_lang", "ru")
]))
async def language_menu_handler(message: Message):
    user_id = message.from_user.id
    lang = await get_user_language(user_id) or "en"
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=lang_name)] for lang_name in languages.values()],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(get_text("choose_language", lang), reply_markup=kb)

# --- 2. Til tanlanganda (reply keyboard orqali)
@router.message(lambda msg: msg.text and msg.text.strip() in languages.values())
async def language_selected_handler(message: Message):
    user_id = message.from_user.id
    # Qaysi til tanlandi?
    lang_code = next((k for k, v in languages.items() if v == message.text.strip()), "en")
    await save_user_language(user_id, lang_code)
    await message.answer(
        get_text("language_selected", lang_code),
        reply_markup=get_main_keyboard(lang_code)
    )

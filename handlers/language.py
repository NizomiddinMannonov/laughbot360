from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Text
from services.database import save_user_language, get_user_language
from localization.texts import texts
from keyboards.reply import get_main_keyboard  # ✅ BONUS TAKLIF

router = Router()

# 🌐 Tilni o‘zgartirish menyusi
@router.message(Text(text=["🌐 Tilni o‘zgartirish", "🌐 Change Language", "🌐 Изменить язык"]))
async def show_language_menu(message: Message):
    user_id = message.from_user.id
    lang = get_user_language(user_id) or "en"

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇺🇿 O‘zbek tili")],
            [KeyboardButton(text="🇷🇺 Русский язык")],
            [KeyboardButton(text="🇬🇧 English")]
        ],
        resize_keyboard=True
    )

    await message.answer(texts[lang]["choose_language"], reply_markup=keyboard)

# 🇺🇿 🇷🇺 🇬🇧 Til tanlanganda qayta menyu chiqarish
@router.message(Text(text=["🇺🇿 O‘zbek tili", "🇷🇺 Русский язык", "🇬🇧 English"]))
async def handle_language_selection(message: Message):
    user_id = message.from_user.id
    selected_text = message.text

    lang_code = "en"
    if "O‘zbek" in selected_text:
        lang_code = "uz"
    elif "Русский" in selected_text:
        lang_code = "ru"

    save_user_language(user_id, lang_code)

    await message.answer(
        texts[lang_code]["lang_selected"],
        reply_markup=get_main_keyboard(lang_code)  # ✅ BONUS TAKLIF ISHLATILDI
    )

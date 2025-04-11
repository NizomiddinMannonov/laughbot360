# 📁 keyboards/reply.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from localization.texts import texts

# 🌐 Asosiy menyu tugmalari (tilga qarab)
def get_main_keyboard(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=texts[lang]["meme"])],
            [KeyboardButton(text=texts[lang]["change_lang"])]
        ],
        resize_keyboard=True
    )

# 🌐 Til tanlash uchun maxsus tugmalar
def get_language_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text="🇺🇿 Uzbek (O‘zbek)")],
        [KeyboardButton(text="🇬🇧 English")],
        [KeyboardButton(text="🇷🇺 Русский")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True
    )
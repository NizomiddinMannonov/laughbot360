from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from localization.texts import texts

def get_main_keyboard(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=texts[lang]["meme"])],
            [KeyboardButton(text=texts[lang]["smart_meme"])],
            [KeyboardButton(text=texts[lang]["change_lang"])]
        ],
        resize_keyboard=True
    )

def get_language_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text="🇺🇿 O‘zbek tili")],
        [KeyboardButton(text="🇬🇧 English")],
        [KeyboardButton(text="🇷🇺 Русский язык")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True
    )

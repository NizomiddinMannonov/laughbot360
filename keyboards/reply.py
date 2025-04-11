from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from localization.texts import texts

def get_main_keyboard(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=texts[lang]["meme"])
            ],
            [KeyboardButton(text=texts[lang]["change_lang"])]
        ],
        resize_keyboard=True
    )

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from localization.texts import get_text

# Asosiy menyu klaviaturasi (zamonaviy grid)
def get_main_keyboard(lang: str) -> ReplyKeyboardMarkup:
    """
    Foydalanuvchining tanlangan tiliga mos asosiy menyu (2x2 tugma) klaviaturasi.
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=get_text("meme", lang)),
                KeyboardButton(text=get_text("smart_meme", lang))
            ],
            [
                KeyboardButton(text=get_text("my_history", lang)),
                KeyboardButton(text=get_text("change_lang", lang))
            ]
        ],
        resize_keyboard=True  # Har doim ekranga moslashadi
    )

# Til tanlash klaviaturasi (flag + nom)
LANGS = {
    "en": "🇬🇧 English",
    "uz": "🇺🇿 O‘zbek tili",
    "ru": "🇷🇺 Русский язык"
}

def get_language_keyboard() -> ReplyKeyboardMarkup:
    """
    Til tanlash uchun universal, 1ta ustunda flagli klaviatura.
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=lang_name)]
            for lang_name in LANGS.values()
        ],
        resize_keyboard=True,
        one_time_keyboard=True  # Tanlagandan keyin avtomatik yopiladi
    )

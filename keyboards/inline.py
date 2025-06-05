from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from localization.texts import get_text

def get_meme_inline_buttons(lang: str, prompt_id: str, like_count=0, dislike_count=0) -> InlineKeyboardMarkup:
    """
    Asosiy meme uchun Like/Dislike/Remix tugmalari (lokalizatsiya va statistikalar bilan).
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f"👍 {like_count}",
                callback_data=f"like|{prompt_id}"
            ),
            InlineKeyboardButton(
                text=f"👎 {dislike_count}",
                callback_data=f"dislike|{prompt_id}"
            ),
            InlineKeyboardButton(
                text=get_text("remix", lang),
                callback_data=f"remix|{prompt_id}"
            )
        ]
    ])

def get_remix_inline_buttons(lang: str, prompt_id: str, like_count=0, dislike_count=0) -> InlineKeyboardMarkup:
    """
    Remix javoblari uchun ham xuddi shunday tugmalar.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f"👍 {like_count}",
                callback_data=f"like|{prompt_id}"
            ),
            InlineKeyboardButton(
                text=f"👎 {dislike_count}",
                callback_data=f"dislike|{prompt_id}"
            ),
            InlineKeyboardButton(
                text=get_text("remix", lang),
                callback_data=f"remix|{prompt_id}"
            )
        ]
    ])

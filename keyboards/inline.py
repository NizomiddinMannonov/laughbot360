from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Remix tugmalari
def get_remix_inline_buttons(prompt_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="👍 Like", callback_data="like"),
            InlineKeyboardButton(text="👎 Dislike", callback_data="dislike"),
            InlineKeyboardButton(text="🔄 Remix", callback_data=f"remix|{prompt_id}")
        ],
        [
            InlineKeyboardButton(text="📤 Share", switch_inline_query="Remix me!")
        ]
    ])

# Mem tugmalari
def get_meme_inline_buttons() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="👍 Like", callback_data="like"),
            InlineKeyboardButton(text="👎 Dislike", callback_data="dislike"),
            InlineKeyboardButton(text="🔄 Remix", callback_data="remix")
        ],
        [
            InlineKeyboardButton(text="📤 Share", switch_inline_query="Share me!")
        ]
    ])

import json
import os

TEXTS_PATH = os.path.join(os.path.dirname(__file__), "texts.json")

with open(TEXTS_PATH, 'r', encoding='utf-8') as f:
    texts = json.load(f)

DEFAULT_LANG = 'en'

def get_text(key: str, lang: str = DEFAULT_LANG) -> str:
    """Berilgan kalit va til bo‘yicha matnni oladi."""
    return texts.get(lang, {}).get(key) \
        or texts.get(DEFAULT_LANG, {}).get(key, f'{{{key}}}')

# Barcha tugma matnlarini universal olish — hammasini!
KB_KEYS = [
    "meme",
    "smart_meme",
    "change_lang",
    "my_history",
    "settings"
]

ALL_KB_TEXTS = sorted({  # Set: dublikat yo‘q, sorted: tartibli
    text
    for lang_dict in texts.values()
    for key in KB_KEYS
    if (text := lang_dict.get(key, ""))
    and text.strip()
})

# (Agar reply tugmalar o‘zgarsa — KB_KEYS ga yangi kalit qo‘shing!)


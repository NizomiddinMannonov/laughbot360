# handlers/language_callback.py

from aiogram import Router, F
from aiogram.types import CallbackQuery
from services.database import save_user_language
from localization.texts import texts
from keyboards.reply import get_main_keyboard

router = Router()

@router.callback_query(F.data.startswith("lang:"))
async def handle_language_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    data = callback.data  # lang:uz, lang:en, lang:ru
    lang_code = data.split(":")[1]

    # Saqlash
    save_user_language(user_id, lang_code)

    # Javob
    await callback.message.edit_text(
        texts[lang_code]["lang_selected"],
        reply_markup=None  # Inline tugmalarni olib tashlaymiz
    )

    # Asosiy menyu chiqarish
    await callback.message.answer(
        texts[lang_code]["main_menu"],
        reply_markup=get_main_keyboard(lang_code)
    )

    # Callback queryni javoblash ("loading" effektni yo'qotish)
    await callback.answer()

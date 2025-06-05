from aiogram import Router, F
from aiogram.types import CallbackQuery
from services.database import save_user_language
from localization.texts import get_text
from keyboards.reply import get_main_keyboard
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.callback_query(F.data.startswith("lang:"))
async def handle_language_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    data = callback.data  # lang:uz, lang:en, lang:ru
    lang_code = data.split(":", 1)[1]

    # Faqat mavjud tillarni ruxsat beramiz
    if lang_code not in ["en", "uz", "ru"]:
        lang_code = "en"

    try:
        await save_user_language(user_id, lang_code)
        # Inline keyboarddan keyin matnni tahrirlash (reply markup o‘chirilsin)
        await callback.message.edit_text(
            get_text("lang_selected", lang_code),
            reply_markup=None
        )
        # Yangi til bilan asosiy menyuni ko‘rsatish
        await callback.message.answer(
            get_text("main_menu", lang_code),
            reply_markup=get_main_keyboard(lang_code)
        )
        # Callbackni tugatamiz
        await callback.answer()
    except Exception as e:
        logger.exception(f"Language callback error: {e}")
        await callback.message.answer(
            get_text("error", lang_code).format(error=str(e)),
            reply_markup=get_main_keyboard(lang_code)
        )
        await callback.answer()

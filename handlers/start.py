from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from services.database import get_user_language, add_user
from localization.texts import get_text
from keyboards.reply import get_main_keyboard

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    user_id = message.from_user.id
    lang = await get_user_language(user_id)
    if not lang:
        lang = "en"
        await add_user(user_id, lang)  # Foydalanuvchini ro‘yxatga olamiz (birinchi kirgan bo‘lsa)

    await message.answer(
        get_text("start", lang),
        reply_markup=get_main_keyboard(lang)
    )

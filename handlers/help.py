from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from services.database import get_user_language
from keyboards.reply import get_main_keyboard

router = Router()

HELP_TEXTS = {
    "en": (
        "ℹ️ <b>Laughbot360</b> — your AI-powered meme creation bot.\n\n"
        "⚙️ Available commands:\n"
        "/start – Start the bot\n"
        "/meme – Create a simple meme\n"
        "/smartmeme – Create a smart meme (caption + image idea)\n"
        "/settings – Change language\n"
        "/myhistory – My meme history\n"
        "/help – Help\n"
    ),
    "uz": (
        "ℹ️ <b>Laughbot360</b> — AI yordamida mem yaratadigan Telegram bot.\n\n"
        "⚙️ Mavjud buyruqlar:\n"
        "/start – Botni ishga tushirish\n"
        "/meme – Oddiy mem yaratish\n"
        "/smartmeme – Aqlli mem yaratish (matn + tasvir)\n"
        "/settings – Tilni o‘zgartirish\n"
        "/myhistory – Tarixim\n"
        "/help – Yordam\n"
    ),
    "ru": (
        "ℹ️ <b>Laughbot360</b> — бот для создания мемов с помощью AI.\n\n"
        "⚙️ Доступные команды:\n"
        "/start – Запустить бота\n"
        "/meme – Создать обычный мем\n"
        "/smartmeme – Умный мем (текст + описание изображения)\n"
        "/settings – Изменить язык\n"
        "/myhistory – Моя история\n"
        "/help – Помощь\n"
    )
}

@router.message(Command("help"))
async def handle_help(message: Message):
    user_id = message.from_user.id
    lang = await get_user_language(user_id) or "en"
    help_text = HELP_TEXTS.get(lang, HELP_TEXTS["en"])
    await message.answer(help_text, reply_markup=get_main_keyboard(lang))

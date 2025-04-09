# handlers/ai.py

from aiogram import Router, F
from aiogram.types import Message
from services.ai_response import get_chatgpt_response

router = Router()

@router.message(F.text)
async def ai_chat_handler(message: Message):
    user_input = message.text
    await message.answer("🤔 Javob tayyorlanmoqda...")

    # AI javobni chaqirish
    response = await get_chatgpt_response(user_input)

    await message.answer(response)

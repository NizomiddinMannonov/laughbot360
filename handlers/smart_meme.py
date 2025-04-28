from aiogram import Router, F, Bot
from aiogram.types import Message, BufferedInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import asyncio

from services.database import get_user_language, check_user_daily_limit, users_collection as db, save_prompt
from services.ai_response import generate_meme_caption
from services.image_editor import create_dalle_meme_image
from localization.texts import texts
from keyboards.reply import get_main_keyboard

router = Router()

class SmartMemeStates(StatesGroup):
    waiting_for_caption = State()
    waiting_for_description = State()

# ✨ Smart Meme boshlash
@router.message(F.text.in_([
    texts["en"]["smart_meme"],
    texts["uz"]["smart_meme"],
    texts["ru"]["smart_meme"]
]))
async def start_smart_meme(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_user_language(user_id) or "en"

    await state.clear()
    await state.set_state(SmartMemeStates.waiting_for_caption)

    await message.answer(
        texts[lang]["caption_prompt"],
        reply_markup=get_main_keyboard(lang)
    )

# 📝 Foydalanuvchidan mem matnini olish
@router.message(SmartMemeStates.waiting_for_caption, F.text)
async def receive_caption(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_user_language(user_id) or "en"

    # Agar foydalanuvchi tugma textini yuborsa rad etamiz
    if message.text in [
        texts["en"]["smart_meme"],
        texts["uz"]["smart_meme"],
        texts["ru"]["smart_meme"]
    ]:
        await message.answer("📝 Iltimos, mem uchun haqiqiy matn yuboring.")
        return

    await state.update_data(caption=message.text)
    await state.set_state(SmartMemeStates.waiting_for_description)

    await message.answer(
        texts[lang]["image_description_prompt"],
        reply_markup=get_main_keyboard(lang)
    )

# 🖼 Tasvirni qabul qilish va AI bilan rasm va caption yaratish
@router.message(SmartMemeStates.waiting_for_description, F.text)
async def generate_smart_meme(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_user_language(user_id) or "en"

    user_data = await state.get_data()
    caption_prompt = user_data.get("caption")
    image_description = message.text

    allowed, remaining = check_user_daily_limit(db, user_id, daily_limit=3)
    if not allowed:
        await message.answer(texts[lang]["daily_limit_exceeded"])
        await state.clear()
        return

    await message.answer(texts[lang]["generating_response"])

    try:
        meme_caption = await generate_meme_caption(caption_prompt, lang)
        if not meme_caption:
            meme_caption = "😅 AI caption yaratishda muammo bo‘ldi."

        image: BufferedInputFile = await create_dalle_meme_image(image_description, lang)
        prompt_id = save_prompt(image_description)

        markup = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="👍 Like", callback_data="like"),
                InlineKeyboardButton(text="👎 Dislike", callback_data="dislike"),
                InlineKeyboardButton(text="🔄 Remix", callback_data=f"remix|{prompt_id}")
            ]
        ])

        await message.answer_photo(
            photo=image,
            caption=f"{meme_caption}\n\n{texts[lang]['remaining_attempts'].format(remaining=remaining)}",
            reply_markup=markup
        )

    except Exception as e:
        await message.answer(texts[lang]["error"].format(error=str(e)))

    await state.clear()

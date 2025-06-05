from aiogram import Router, F, Bot
from aiogram.types import Message, BufferedInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import logging

from services.database import get_user_language, check_user_daily_limit, save_meme
from services.ai_response import generate_meme_caption
from services.image_editor import create_dalle_meme_image
from localization.texts import get_text
from keyboards.reply import get_main_keyboard

logger = logging.getLogger(__name__)
router = Router()

class SmartMemeStates(StatesGroup):
    waiting_for_caption = State()
    waiting_for_description = State()

@router.message(F.text.in_([
    get_text("smart_meme", "en"),
    get_text("smart_meme", "uz"),
    get_text("smart_meme", "ru")
]))
async def start_smart_meme(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = await get_user_language(user_id) or "en"

    await state.clear()
    await state.set_state(SmartMemeStates.waiting_for_caption)
    await message.answer(
        get_text("caption_prompt", lang),
        reply_markup=get_main_keyboard(lang)
    )

@router.message(SmartMemeStates.waiting_for_caption, F.text)
async def receive_caption(message: Message, state: FSMContext):
    lang = await get_user_language(message.from_user.id) or "en"
    text = message.text.strip()

    if text in [
        get_text("smart_meme", "en"),
        get_text("smart_meme", "uz"),
        get_text("smart_meme", "ru")
    ] or not text or len(text) < 3:
        await message.answer(get_text("invalid_caption_warning", lang))
        return

    await state.update_data(caption=text)
    await state.set_state(SmartMemeStates.waiting_for_description)
    await message.answer(
        get_text("image_description_prompt", lang),
        reply_markup=get_main_keyboard(lang)
    )

@router.message(SmartMemeStates.waiting_for_description, F.text)
async def generate_smart_meme(message: Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    lang = await get_user_language(user_id) or "en"
    image_description = message.text.strip()
    user_data = await state.get_data()
    caption_prompt = (user_data.get("caption") or "").strip()

    allowed, remaining = await check_user_daily_limit(user_id, daily_limit=3)
    if not allowed:
        await message.answer(get_text("daily_limit_exceeded", lang))
        await state.clear()
        return

    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    loader_msg = await message.answer(get_text("generating_response", lang))

    try:
        # 1. Caption AI orqali generatsiya qilinadi
        meme_caption = await generate_meme_caption(caption_prompt, lang)
        if not meme_caption or len(meme_caption) < 2:
            meme_caption = get_text("ai_caption_error", lang)
        # 2. DALL·E orqali rasm yaratiladi
        image: BufferedInputFile = await create_dalle_meme_image(image_description, lang)

        # 3. Rasm yuboriladi
        sent_msg = await message.answer_photo(
            photo=image,
            caption=f"{meme_caption}\n\n{get_text('remaining_attempts', lang).format(remaining=remaining)}"
        )
        # 4. file_id olinadi va faqat bitta marta DB ga saqlanadi
        photo_file_id = sent_msg.photo[-1].file_id if sent_msg.photo else None
        meme_id = await save_meme(user_id, photo_file_id, meme_caption, image_description)

        # 5. Inline tugmalarini edit qilamiz
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text=f"👍 0", callback_data=f"like|{meme_id}"),
                InlineKeyboardButton(text=f"👎 0", callback_data=f"dislike|{meme_id}"),
                InlineKeyboardButton(text=get_text("remix", lang), callback_data=f"remix|{meme_id}")
            ]
        ])
        await sent_msg.edit_reply_markup(reply_markup=markup)
        await loader_msg.delete()

    except Exception as e:
        logger.exception(f"Smart meme error: {e}")
        await loader_msg.edit_text(get_text("error", lang).format(error=str(e)))
    finally:
        await state.clear()

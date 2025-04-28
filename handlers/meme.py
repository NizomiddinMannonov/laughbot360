from aiogram import Router, F, Bot
from aiogram.types import Message, BufferedInputFile, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import asyncio

from services.database import get_user_language, check_user_daily_limit, users_collection as db, save_prompt, get_prompt_by_id
from services.ai_response import generate_meme_caption, generate_remix_message
from services.image_editor import create_dalle_meme_image
from localization.texts import texts
from keyboards.reply import get_main_keyboard

router = Router()

class MemeStates(StatesGroup):
    waiting_for_caption = State()

@router.message(F.text.in_([
    texts["en"]["meme"],
    texts["uz"]["meme"],
    texts["ru"]["meme"]
]))
async def start_meme_creation(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_user_language(user_id) or "en"

    await state.clear()
    await state.set_state(MemeStates.waiting_for_caption)

    await message.answer(
        texts[lang]["ask_for_meme_text"],
        reply_markup=get_main_keyboard(lang)
    )

@router.message(MemeStates.waiting_for_caption)
async def handle_meme_prompt(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_user_language(user_id) or "en"

    prompt = message.text or message.caption
    if not prompt or not prompt.strip():
        await message.answer(texts[lang]["invalid_caption_warning"])
        return
    if len(prompt.strip()) < 3:
        await message.answer(texts[lang]["invalid_caption_warning"])
        return

    allowed, remaining = check_user_daily_limit(db, user_id, daily_limit=3)
    if not allowed:
        await message.answer(texts[lang]["daily_limit_exceeded"])
        await state.clear()
        return

    await message.answer(texts[lang]["generating_response"])

    try:
        caption = await generate_meme_caption(prompt, lang)
        image: BufferedInputFile = await create_dalle_meme_image(prompt, lang)
        prompt_id = save_prompt(prompt)

        markup = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="👍 Like", callback_data="like"),
                InlineKeyboardButton(text="👎 Dislike", callback_data="dislike"),
                InlineKeyboardButton(text="🔄 Remix", callback_data=f"remix|{prompt_id}")
            ]
        ])

        await message.answer_photo(
            photo=image,
            caption=f"{caption}\n\n{texts[lang]['remaining_attempts'].format(remaining=remaining)}",
            reply_markup=markup
        )

    except Exception as e:
        await message.answer(texts[lang]["error"].format(error=str(e)))

    await state.clear()

@router.callback_query(F.data.startswith("remix|"))
async def handle_remix(callback: CallbackQuery, bot: Bot):
    lang = get_user_language(callback.from_user.id) or "en"
    _, prompt_id = callback.data.split("|", 1)
    prompt = get_prompt_by_id(prompt_id)

    if not prompt:
        await callback.message.answer(texts[lang]["error"].format(error="Prompt not found"))
        return

    allowed, remaining = check_user_daily_limit(db, callback.from_user.id, daily_limit=3)
    if not allowed:
        await callback.message.answer(texts[lang]["daily_limit_exceeded"])
        return

    remix_msg = await generate_remix_message(prompt, lang)
    await callback.answer(texts[lang]["generating_response"])

    await bot.send_chat_action(chat_id=callback.message.chat.id, action="typing")
    await asyncio.sleep(1.2)

    image: BufferedInputFile = await create_dalle_meme_image(prompt, lang)
    caption = f"{remix_msg}\n\n{texts[lang]['remix_info'].format(remaining=remaining)}"

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="👍 Like", callback_data="like"),
            InlineKeyboardButton(text="👎 Dislike", callback_data="dislike"),
            InlineKeyboardButton(text="🔄 Remix", callback_data=f"remix|{prompt_id}")
        ]
    ])

    await callback.message.answer_photo(
        photo=image,
        caption=caption,
        reply_markup=markup
    )

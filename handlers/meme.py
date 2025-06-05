from aiogram import Router, F, Bot
from aiogram.types import (
    Message, BufferedInputFile, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import logging

from services.database import (
    get_user_language, check_user_daily_limit, save_prompt, get_prompt_by_id,
    add_meme_vote, get_meme_stats, has_voted, save_meme
)
from services.ai_response import generate_meme_caption, generate_remix_message
from services.image_editor import create_dalle_meme_image
from localization.texts import get_text, ALL_KB_TEXTS
from keyboards.reply import get_main_keyboard

logger = logging.getLogger(__name__)
router = Router()

class MemeStates(StatesGroup):
    waiting_for_caption = State()

def is_kb_text(text: str) -> bool:
    """Bu funksiya tugmalardagi matnlarni aniqlaydi."""
    return text in ALL_KB_TEXTS

def meme_markup(lang, prompt_id, like_count=0, dislike_count=0):
    """Mem uchun interaktiv tugmalar yaratadi."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f"👍 {like_count}", callback_data=f"like|{prompt_id}"),
            InlineKeyboardButton(text=f"👎 {dislike_count}", callback_data=f"dislike|{prompt_id}"),
            InlineKeyboardButton(text=get_text("remix", lang), callback_data=f"remix|{prompt_id}")
        ]
    ])

# --- Like/Dislike Callback ---
@router.callback_query(F.data.regexp(r"^(like|dislike)\|"))
async def handle_vote(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    lang = await get_user_language(user_id) or "en"
    action, prompt_id = callback.data.split("|", 1)

    prev_vote = await has_voted(prompt_id, user_id)
    if prev_vote == action:
        await callback.answer(get_text("already_voted", lang), show_alert=True)
        return

    await callback.answer(get_text("vote_processing", lang))
    await add_meme_vote(prompt_id, user_id, action)
    like_count, dislike_count = await get_meme_stats(prompt_id)
    markup = meme_markup(lang, prompt_id, like_count, dislike_count)
    try:
        await callback.message.edit_reply_markup(reply_markup=markup)
    except Exception:
        pass

# --- Remix Callback ---
@router.callback_query(F.data.regexp(r"^remix\|"))
async def handle_remix(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    lang = await get_user_language(user_id) or "en"
    _, prompt_id = callback.data.split("|", 1)
    prompt = await get_prompt_by_id(prompt_id)

    # Darhol loader va xabar chiqaring!
    await callback.answer(get_text("generating_response", lang))
    
    allowed, remaining = await check_user_daily_limit(user_id, daily_limit=3)
    if not allowed:
        await callback.answer(get_text("daily_limit_exceeded", lang), show_alert=True)
        return

    loader_msg = await callback.message.answer(get_text("generating_response", lang))
    try:
        remix_msg = await generate_remix_message(prompt, lang)
        image: BufferedInputFile = await create_dalle_meme_image(prompt, lang)
        remix_prompt_id = await save_prompt(prompt, user_id=user_id)
        like_count, dislike_count = await get_meme_stats(remix_prompt_id)
        markup = meme_markup(lang, remix_prompt_id, like_count, dislike_count)

        await callback.message.answer_photo(
            photo=image,
            caption=f"{remix_msg}\n\n{get_text('remix_info', lang).format(remaining=remaining)}",
            reply_markup=markup
        )
        await loader_msg.delete()
    except Exception as e:
        await loader_msg.edit_text(f"Remix error: {e}")
        await callback.answer(str(e), show_alert=True)  # Qo‘shimcha xatolik xabari

# --- Main meme creation (optimal, loaderli) ---
@router.message()
async def meme_router_handler(message: Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    lang = await get_user_language(user_id) or "en"
    text = (message.text or message.caption or "").strip()

    if is_kb_text(text):
        await state.clear()
        if text == get_text("meme", lang):
            await state.set_state(MemeStates.waiting_for_caption)
            await message.answer(get_text("ask_for_meme_text", lang), reply_markup=get_main_keyboard(lang))
            return
        return

    current_state = await state.get_state()
    if current_state == MemeStates.waiting_for_caption.state:
        prompt = text
        if not prompt or len(prompt) < 3:
            await message.answer(get_text("invalid_caption_warning", lang))
            return
        allowed, remaining = await check_user_daily_limit(user_id, daily_limit=3)
        if not allowed:
            await message.answer(get_text("daily_limit_exceeded", lang))
            await state.clear()
            return

        await bot.send_chat_action(chat_id=message.chat.id, action="typing")
        loader_msg = await message.answer(get_text("generating_response", lang))

        try:
            caption = await generate_meme_caption(prompt, lang)
            image: BufferedInputFile = await create_dalle_meme_image(prompt, lang)
            # prompt_id = await save_prompt(prompt, user_id=user_id)  # endi kerak emas
            # Like/dislike uchun birinchi marta 0 bo‘ladi
            markup = meme_markup(lang, "noid", 0, 0)
            sent_msg = await message.answer_photo(
                photo=image,
                caption=f"{caption}\n\n{get_text('remaining_attempts', lang).format(remaining=remaining-1)}",
                reply_markup=markup
            )
            # Yangi rasm yuborilgandan keyin file_id ni olamiz:
            photo_file_id = sent_msg.photo[-1].file_id if sent_msg.photo else None
            # Bazaga rasmni, file_id ni, caption va promptni saqlaymiz
            meme_id = await save_meme(user_id, photo_file_id, caption, prompt)
            # Endi tugmalarni real meme_id bilan yangilaymiz
            like_count, dislike_count = await get_meme_stats(meme_id)
            markup = meme_markup(lang, meme_id, like_count, dislike_count)
            await sent_msg.edit_reply_markup(reply_markup=markup)
            await loader_msg.delete()
        except Exception as e:
            await loader_msg.edit_text(f"⚠️ Error: {e}")
            logger.exception("Meme creation error: %s", e)
        finally:
            await state.clear()
        return

    await message.answer(get_text("main_menu", lang), reply_markup=get_main_keyboard(lang))
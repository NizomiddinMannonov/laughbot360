from aiogram import Router, F
from aiogram.types import Message, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from services.database import get_user_language
from services.ai_response import generate_meme_caption
from services.image_editor import create_dalle_meme_image
from localization.texts import texts
from keyboards.reply import get_main_keyboard

router = Router()

class MemeStates(StatesGroup):
    waiting_for_caption = State()

# 🖼 Mem yaratishni boshlash
@router.message(F.text.in_([
    "🖼 Mem yaratish",
    "🖼 Create Meme",
    "🖼 Создать мем"
]))
async def start_meme_creation(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_user_language(user_id)

    await state.clear()
    await state.set_state(MemeStates.waiting_for_caption)

    await message.answer(
        texts[lang]["ask_for_meme_text"],
        reply_markup=get_main_keyboard(lang)
    )

# 🖼 Matn kelganda mem yaratish
@router.message(MemeStates.waiting_for_caption)
async def handle_meme_prompt(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_user_language(user_id)
    prompt = message.text or message.caption

    await message.answer(texts[lang]["generating_response"])

    try:
        caption = await generate_meme_caption(prompt, lang)
        image: BufferedInputFile = await create_dalle_meme_image(prompt, lang)

        await message.answer_photo(
            photo=image,
            caption=caption,
            reply_markup=get_main_keyboard(lang)
        )

    except Exception as e:
        error_text = str(e)
        if "content_policy_violation" in error_text:
            await message.answer(
                "🚨 Promptingiz xavfsizlik talablariga javob bermadi. "
                "Iltimos, boshqa matn kiriting.\n\n"
                "⚠️ Tavsiya:\n"
                "- Salbiy, siyosiy yoki zo'ravonlik mazmunidagi mavzularni ishlatmang.\n"
                "- Sodda, neytral va ijobiy mavzularni tanlang "
                "(masalan: hayvonlar, tabiat, hazillar yoki oddiy hayotiy vaziyatlar)."
            )
        else:
            await message.answer(texts[lang]["error"].format(error=error_text))

    await state.clear()


    await state.clear()

from aiogram import Router
from aiogram.types import Message, InputMediaPhoto
from services.database import get_user_memes, get_user_language
from localization.texts import get_text

router = Router()

HISTORY_TRIGGERS = set([
    get_text("my_history", "en"),
    get_text("my_history", "uz"),
    get_text("my_history", "ru"),
    "/myhistory",
])

@router.message(lambda msg: (msg.text or "").strip() in HISTORY_TRIGGERS)
async def my_history_handler(message: Message):
    print("[DEBUG HISTORY] Got:", repr(message.text))
    user_id = message.from_user.id
    lang = await get_user_language(user_id) or "en"
    memes = await get_user_memes(user_id, limit=5)
    print("[DEBUG HISTORY] Memes:", memes)
    if not memes:
        await message.answer(get_text("no_history", lang))
        return
    if len(memes) > 1:
        media = [
            InputMediaPhoto(
                media=meme["file_id"],
                caption=f"{meme['caption']}\n🕒 {meme['created_at'].strftime('%Y-%m-%d %H:%M')}"
            ) for meme in memes if meme.get("file_id")
        ]
        await message.answer_media_group(media)
    else:
        meme = memes[0]
        await message.answer_photo(
            photo=meme["file_id"],
            caption=f"{meme['caption']}\n🕒 {meme['created_at'].strftime('%Y-%m-%d %H:%M')}"
        )

import io
import logging
from aiogram.types import BufferedInputFile

from services.ai_response import generate_meme_caption, generate_meme_image
from services.image_editor import add_caption_to_image

logger = logging.getLogger(__name__)

async def generate_ai_meme(user_prompt: str, lang: str = "en") -> BufferedInputFile:
    """
    AI yordamida meme caption va AI rasm generatsiyasi va ularni birlashtirib,
    Telegram uchun BufferedInputFile tarzida qaytaradi.
    :param user_prompt: Foydalanuvchi prompti
    :param lang: Til kodi (en/uz/ru)
    :return: BufferedInputFile
    """
    try:
        # 1. Meme caption yaratish
        caption = await generate_meme_caption(user_prompt, lang)
        # 2. AI yordamida rasm generatsiyasi
        ai_image_io = await generate_meme_image(user_prompt, lang)  # io.BytesIO qaytaradi
        # 3. Rasmga caption yozib qo‘yish (sync funksiya bo‘lsa)
        meme_io = add_caption_to_image(ai_image_io.read(), caption, position="bottom")
        # 4. Telegram uchun BufferedInputFile qilish
        meme_file = BufferedInputFile(meme_io.getvalue(), filename="meme.jpg")
        return meme_file
    except Exception as e:
        logger.error(f"Meme generation error: {e}")
        raise

async def user_image_with_caption(user_image_bytes: bytes, caption: str) -> BufferedInputFile:
    """
    Foydalanuvchi yuborgan rasmga caption qo‘yadi va Telegram uchun BufferedInputFile qaytaradi.
    """
    try:
        meme_io = add_caption_to_image(user_image_bytes, caption, position="bottom")
        meme_file = BufferedInputFile(meme_io.getvalue(), filename="meme.jpg")
        return meme_file
    except Exception as e:
        logger.error(f"User meme generation error: {e}")
        raise

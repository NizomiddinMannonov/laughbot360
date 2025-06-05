import io
import logging
from PIL import Image, ImageDraw, ImageFont

from services.ai_response import generate_meme_image, MemeImageError

logger = logging.getLogger(__name__)

# 1. DALL·E yoki boshqa AI orqali mem rasmini yaratish (aiogram uchun)
async def create_dalle_meme_image(prompt: str, lang: str = "en"):
    """
    DALL·E orqali mem rasm yaratadi va aiogram uchun BufferedInputFile qaytaradi.
    """
    try:
        image_bytes_io = await generate_meme_image(prompt, lang)
        from aiogram.types import BufferedInputFile
        image_bytes_io.seek(0)
        return BufferedInputFile(
            file=image_bytes_io.read(),
            filename="meme.png"
        )
    except MemeImageError as e:
        logger.error(f"❌ MemeImageError: {e}")
        raise
    except Exception as e:
        logger.error(f"❌ Error in create_dalle_meme_image: {e}")
        raise MemeImageError(str(e))

# 2. Rasmga caption (matn) qo‘yish, BytesIO tarzda
def add_caption_to_image(image_bytes: bytes, caption: str, position: str = "top") -> io.BytesIO:
    """
    Rasmga matn (caption) yozib, BytesIO qaytaradi.
    :param image_bytes: Telegramdan kelgan rasm (bytes)
    :param caption: Qo'yiladigan matn
    :param position: 'top' yoki 'bottom'
    :return: BytesIO (Telegramga yuborish uchun)
    """
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        draw = ImageDraw.Draw(image)
        font_size = max(18, int(image.height * 0.06))
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except Exception:
            font = ImageFont.load_default()

        # Matnni o‘rtaga joylashtirish
        text_width, text_height = draw.textsize(caption, font=font)
        x = (image.width - text_width) // 2
        y = 10 if position == "top" else image.height - text_height - 20

        # Kontur (outline) uchun
        outline = 2
        for ox in range(-outline, outline + 1):
            for oy in range(-outline, outline + 1):
                draw.text((x + ox, y + oy), caption, font=font, fill="black")
        draw.text((x, y), caption, font=font, fill="white")

        output = io.BytesIO()
        image.save(output, format='JPEG')
        output.seek(0)
        return output
    except Exception as e:
        logger.error(f"Image caption error: {e}")
        raise

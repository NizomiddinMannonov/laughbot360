from PIL import Image, ImageDraw, ImageFont
import io
import base64
from aiogram.types import BufferedInputFile
from openai import AsyncOpenAI

client = AsyncOpenAI()

# 🎨 Oddiy mem rasm yaratish
async def create_meme_image(caption: str) -> BufferedInputFile:
    image = Image.new("RGB", (800, 600), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 36)
    except:
        font = ImageFont.load_default()

    text_bbox = draw.textbbox((0, 0), caption, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (800 - text_width) // 2
    y = (600 - text_height) // 2
    draw.text((x, y), caption, font=font, fill=(0, 0, 0))

    output = io.BytesIO()
    image.save(output, format="PNG")
    output.seek(0)

    return BufferedInputFile(file=output.read(), filename="meme.png")


# 🧠 Matnga kulgili uslub berish (stilize caption)
async def style_caption(prompt: str, lang: str) -> str:
    system_prompt = {
        "en": "You are a meme stylist. Return the same text but funnier using uppercase, emojis, or funny spelling.",
        "uz": "Siz mem stilistisiz. Matnni hazil tarzida, emoji yoki katta harflar bilan chiroyli qilib qaytaring.",
        "ru": "Ты стилист мемов. Верни текст в смешном стиле с эмодзи или капсом."
    }.get(lang, "Make this meme caption funnier and more stylish.")

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8
    )

    return response.choices[0].message.content.strip()


# 🖼 DALL·E yordamida mem rasm generatsiyasi (optimal variant, lang parametri bilan)
async def create_dalle_meme_image(prompt: str, lang: str) -> BufferedInputFile:
    dalle_response = await client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        response_format="b64_json",
        quality="standard",
        n=1
    )

    image_data = dalle_response.data[0].b64_json
    image_bytes = base64.b64decode(image_data)

    return BufferedInputFile(file=image_bytes, filename="ai_meme.png")

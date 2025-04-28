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
        "en": "You are a professional meme stylist.Transform the given text into a funnier, more eye-catching meme caption.Use creative techniques such as: ALL CAPS, emojis, exaggerated spellings, playful tone, and meme slang if needed. Make sure the result feels natural, modern, and highly shareableReturn only the improved meme caption without any explanations.",
        "uz": "Siz professional mem stilistisiz.Berilgan matnni yanada kulgili, ko‘zni qamashtiradigan mem matniga aylantiring.Kreativ usullar qo‘llang: KATTA HARFLAR, emoji, oshirib yozilgan so‘zlar, o‘ynoqi ohang, kerak bo‘lsa meme slenglaridan foydalaning.Natija zamonaviy, tabiiy va tarqalishga yaroqli bo‘lsin.Faqat yaxshilangan mem matnini qaytaring, hech qanday tushuntirish bermang.",
        "ru": "Вы профессиональный стилист мемов.Преобразуйте данный текст в более смешной, яркий и запоминающийся текст для мема.Используйте креативные приёмы: ВСЕ ПРОПИСНЫЕ БУКВЫ, эмодзи, преувеличенные написания, игривый тон, а при необходимости — сленг мемов.Результат должен быть современным, естественным и легко рассылаемым.Верните только улучшенный текст мема без объяснений."

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

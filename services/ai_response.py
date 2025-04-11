import base64
import io
import logging
from openai import AsyncOpenAI
from config import OPENAI_API_KEY

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# 🎨 Mem caption generatsiya funksiyasi
async def generate_meme_caption(prompt: str, lang: str) -> str:
    system_prompt = {
        "en": "You are a meme expert. Return only a short, funny meme caption.",
        "uz": "Siz mem yaratish bo‘yicha mutaxassissiz. Faqat kulgili va qisqa mem matnini qaytaring.",
        "ru": "Ты эксперт по мемам. Верни только короткий и смешной текст мема."
    }.get(lang, "You are a meme expert. Return only a short, funny meme caption.")

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()


# 🖼 Mem uchun rasm generatsiyasi (DALL·E orqali)
async def generate_meme_image(prompt: str, lang: str) -> bytes:
    try:
        response = await client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            response_format="b64_json",
            n=1
        )
        image_data = response.data[0].b64_json
        image_bytes = base64.b64decode(image_data)
        return io.BytesIO(image_bytes)
    except Exception as e:
        logging.error(f"❌ Error generating meme image: {e}")
        raise

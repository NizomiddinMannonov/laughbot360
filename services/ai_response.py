# 📁 services/ai_response.py

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

# 🤖 Remix bosilganda kulgili, kontekstual xabar chiqarish
async def generate_remix_message(prompt: str, lang: str) -> str:
    system_prompt = {
        "uz": (
            "Siz kulgili, o‘zbekona hazil tuyg‘usiga ega sun’iy intellektsiyasiz. "
            "Sizdan remix so‘ralganida, foydalanuvchiga qisqa, quvnoq va hazilkash tarzda javob berasiz. "
            "Javobingiz ichida emoji ishlatsangiz ham bo‘ladi. "
            "Mavzuni o‘zbek madaniyati, kundalik hayot, yoki zamonaviy mem uslubida tasvirlang."
        ),
        "en": (
            "You are a humorous, meme-savvy AI with a clever personality. "
            "When a remix is requested, you respond with a short, witty, and fun message. "
            "You may use emojis. Your reply should feel natural, funny, and fit modern meme culture."
        ),
        "ru": (
            "Ты весёлый и остроумный ИИ, хорошо разбирающийся в мемах. "
            "Когда пользователь просит ремикс, ты отвечаешь короткой, забавной и креативной фразой. "
            "Можно использовать эмодзи. Ответ должен быть уместным, современным и вызывать улыбку."
        )
    }.get(lang, "You are a funny meme remix assistant. Prompt:")

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt + "\nPrompt: " + prompt},
            {"role": "user", "content": "Please reply with a short and funny sentence for remix reaction."}
        ],
        temperature=0.9
    )
    return response.choices[0].message.content.strip()

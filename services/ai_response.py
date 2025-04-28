import base64
import io
import logging
from openai import AsyncOpenAI
from config import OPENAI_API_KEY

# 🎯 OpenAI Client
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# 🎨 1. Meme caption generatsiya qilish
async def generate_meme_caption(prompt: str, lang: str) -> str:
    system_prompts = {
        "en": (
            "You are a professional meme expert. "
            "Generate a short, witty, and funny meme caption based on the user's input. "
            "The caption should feel modern, natural, and shareable."
        ),
        "uz": (
            "Siz professional mem mutaxassisisiz. "
            "Foydalanuvchi yuborgan matn asosida qisqa, kulgili va zamonaviy mem matnini yarating. "
            "Natija tabiiy va tarqalishga yaroqli bo‘lishi kerak."
        ),
        "ru": (
            "Вы профессиональный эксперт по мемам. "
            "Создайте короткий, остроумный и смешной текст мема на основе ввода пользователя. "
            "Результат должен быть современным и легко рассылаемым."
        )
    }
    system_prompt = system_prompts.get(lang, system_prompts["en"])

    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        logging.error(f"❌ Error generating meme caption: {e}")
        return prompt

# 🖼 2. DALL·E orqali rasm generatsiya qilish
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

# 🤖 3. Remix uchun kulgili xabar generatsiya qilish
async def generate_remix_message(prompt: str, lang: str) -> str:
    system_prompts = {
        "en": (
            "You are a humorous, meme-savvy AI assistant. "
            "When asked for a remix, reply with a short, witty, and funny comment. "
            "Use emojis if needed. Make it natural, playful, and modern."
        ),
        "uz": (
            "Siz hazilkash va mem madaniyatidan yaxshi xabardor sun'iy intellektsiyasiz. "
            "Remix so‘ralganda, qisqa va kulgili tarzda javob bering. "
            "Emoji ishlatishingiz mumkin. Javob zamonaviy va hazil ohangida bo‘lishi kerak."
        ),
        "ru": (
            "Вы весёлый и разбирающийся в мемах ИИ. "
            "Когда просят ремикс, отвечайте коротко, остроумно и смешно. "
            "Можно использовать эмодзи. Ответ должен быть современным и игривым."
        )
    }
    system_prompt = system_prompts.get(lang, system_prompts["en"])

    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Prompt: {prompt}\n\nPlease reply with a funny remix comment."}
            ],
            temperature=0.9
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        logging.error(f"❌ Error generating remix message: {e}")
        return "🔄 Remix ready! 🎉"

# ✨ 4. Caption + Tasvirdan DALL·E uchun yuqori sifatli prompt yaratish
async def generate_image_prompt(caption: str, description: str, lang: str = "en") -> str:
    system_prompts = {
        "en": (
            "You are an AI assistant that combines a meme caption and an image description "
            "to create a high-quality English prompt for DALL·E. "
            "The prompt must be clear, vivid, and creative."
        ),
        "uz": (
            "Siz mem matni va rasm tasvirini birlashtirib, DALL·E uchun sifatli inglizcha prompt yaratadigan AI yordamchisisiz. "
            "Prompt aniq, tasavvurga boy va ijodiy bo‘lishi kerak."
        ),
        "ru": (
            "Вы ИИ-ассистент, который объединяет подпись к мему и описание изображения, "
            "чтобы создать качественный англоязычный запрос для DALL·E. "
            "Запрос должен быть четким, ярким и креативным."
        )
    }
    system_prompt = system_prompts.get(lang, system_prompts["en"])

    try:
        user_input = f"Meme Caption: {caption}\nImage Description: {description}"

        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.8
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        logging.error(f"❌ Error generating image prompt: {e}")
        return f"{caption} with {description}"

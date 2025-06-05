import base64
import io
import logging
import asyncio
from openai import AsyncOpenAI
from config import settings

logger = logging.getLogger(__name__)

class MemeAIError(Exception): pass
class MemePromptError(MemeAIError): pass
class MemeCaptionError(MemeAIError): pass
class MemeImageError(MemeAIError): pass

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

# Helper: universal async retry
async def async_retry(fn, *args, retries=2, delay=1, timeout=30, **kwargs):
    for attempt in range(retries + 1):
        try:
            return await asyncio.wait_for(fn(*args, **kwargs), timeout=timeout)
        except Exception as e:
            logger.warning(f"[AI-RETRY] Attempt {attempt+1} failed: {e}")
            if attempt == retries:
                raise
            await asyncio.sleep(delay)

# Meme caption
async def generate_meme_caption(prompt: str, lang: str) -> str:
    system_prompts = {
        # ... system prompt textlari sizda bor ...
        "en": "...",
        "uz": "...",
        "ru": "..."
    }
    system_prompt = system_prompts.get(lang, system_prompts["en"])
    async def inner():
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=64
        )
        result = response.choices[0].message.content.strip()
        if not result:
            raise MemeCaptionError("AI returned empty caption")
        return result

    try:
        return await async_retry(inner)
    except Exception as e:
        logger.error(f"❌ Error generating meme caption: {e}")
        raise MemeCaptionError(f"AI caption error: {e}")

# Meme image (DALL·E)
async def generate_meme_image(prompt: str, lang: str = "en") -> io.BytesIO:
    async def inner():
        response = await client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            response_format="b64_json",
            n=1
        )
        if not response.data or not response.data[0].b64_json:
            raise MemeImageError("AI returned empty image")
        image_data = response.data[0].b64_json
        image_bytes = base64.b64decode(image_data)
        return io.BytesIO(image_bytes)

    try:
        return await async_retry(inner)
    except Exception as e:
        logger.error(f"❌ Error generating meme image: {e}")
        raise MemeImageError(f"AI image error: {e}")

# Meme remix
async def generate_remix_message(prompt: str, lang: str) -> str:
    system_prompts = {
        # ... system prompt textlari sizda bor ...
        "en": "...",
        "uz": "...",
        "ru": "..."
    }
    system_prompt = system_prompts.get(lang, system_prompts["en"])
    async def inner():
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Prompt: {prompt}\n\nPlease reply with a funny remix comment."}
            ],
            temperature=0.9,
            max_tokens=48
        )
        result = response.choices[0].message.content.strip()
        if not result:
            raise MemeCaptionError("AI returned empty remix message")
        return result

    try:
        return await async_retry(inner)
    except Exception as e:
        logger.error(f"❌ Error generating remix message: {e}")
        raise MemeCaptionError(f"AI remix error: {e}")

# Caption + image description -> DALL·E prompt
async def generate_image_prompt(caption: str, description: str, lang: str = "en") -> str:
    system_prompts = {
        # ... system prompt textlari sizda bor ...
        "en": "...",
        "uz": "...",
        "ru": "..."
    }
    system_prompt = system_prompts.get(lang, system_prompts["en"])
    async def inner():
        user_input = f"Meme Caption: {caption}\nImage Description: {description}"
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.8,
            max_tokens=96
        )
        result = response.choices[0].message.content.strip()
        if not result:
            raise MemePromptError("AI returned empty image prompt")
        return result

    try:
        return await async_retry(inner)
    except Exception as e:
        logger.error(f"❌ Error generating image prompt: {e}")
        raise MemePromptError(f"AI prompt error: {e}")

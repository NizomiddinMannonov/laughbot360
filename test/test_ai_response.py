import pytest
import asyncio
from services import ai_response

@pytest.mark.asyncio
async def test_generate_meme_caption_en():
    prompt = "When you see Monday morning"
    lang = "en"
    result = await ai_response.generate_meme_caption(prompt, lang)
    assert isinstance(result, str)
    assert result.strip()  # Bo‘sh bo‘lmasligi uchun

@pytest.mark.asyncio
async def test_generate_meme_caption_uz():
    prompt = "Dushanba tongini ko‘rsang"
    lang = "uz"
    result = await ai_response.generate_meme_caption(prompt, lang)
    assert isinstance(result, str)
    assert result.strip()

@pytest.mark.asyncio
async def test_generate_remix_message_ru():
    prompt = "Когда просишь ремикс"
    lang = "ru"
    result = await ai_response.generate_remix_message(prompt, lang)
    assert isinstance(result, str)
    assert result.strip()

@pytest.mark.asyncio
async def test_generate_image_prompt():
    caption = "That feeling when..."
    description = "A cat in sunglasses on the beach"
    lang = "en"
    result = await ai_response.generate_image_prompt(caption, description, lang)
    assert isinstance(result, str)
    assert "cat" in result.lower()

@pytest.mark.asyncio
async def test_generate_meme_image():
    prompt = "A funny cat meme, trending style, comic, 2024"
    result = await ai_response.generate_meme_image(prompt)
    # Ko‘p AI rasm generatorlar io.BytesIO yoki PIL.Image qaytaradi
    # Shuning uchun quyidagicha tekshirish mumkin:
    if hasattr(result, "read"):
        data = result.read(10)
    elif hasattr(result, "getvalue"):
        data = result.getvalue()
    else:
        data = bytes(result)
    assert len(data) > 0

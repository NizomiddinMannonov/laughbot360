# services/meme_generator.py

import openai
import io
import base64
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

async def generate_meme_image(caption: str):
    if not caption or caption.strip() == "":
        return None

    try:
        response = openai.Image.create(
            model="dall-e-3",
            prompt=f"Create a funny, viral-style meme image with the following caption: '{caption}'",
            size="1024x1024",
            response_format="b64_json"
        )

        image_data = response["data"][0]["b64_json"]
        image_bytes = base64.b64decode(image_data)
        return io.BytesIO(image_bytes)

    except Exception as e:
        print(f"[MEME ERROR] {e}")
        return None
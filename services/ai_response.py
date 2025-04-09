# services/ai_response.py

import openai
from os import getenv
from dotenv import load_dotenv

load_dotenv()
openai.api_key = getenv("OPENAI_API_KEY")

async def get_chatgpt_response(message_text: str, system_prompt: str = "You are a helpful assistant"):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # yoki "gpt-4" agar sizda mavjud bo‘lsa
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message_text}
            ],
            temperature=0.8,
            max_tokens=1000
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"⚠️ Xatolik yuz berdi: {e}"

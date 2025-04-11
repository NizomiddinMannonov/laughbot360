# config.py

import os
from dotenv import load_dotenv

# .env faylni yuklaydi
load_dotenv()

# Telegram bot tokeni
TOKEN = os.getenv("BOT_TOKEN")

# MongoDB Atlas URI
MONGO_URI = os.getenv("MONGO_URI")

# OpenAI API kaliti
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

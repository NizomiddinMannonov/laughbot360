import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

class Settings:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    MONGO_URI: str = os.getenv("MONGO_URI", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    REDIS_URI: str = os.getenv("REDIS_URI", "")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    DAILY_NOTIFICATION_TIME: str = os.getenv("DAILY_NOTIFICATION_TIME", "09:00")
    MEDIA_CHANNEL_ID: str = os.getenv("MEDIA_CHANNEL_ID", "")
    MEDIA_CHANNEL_USERNAME: str = os.getenv("MEDIA_CHANNEL_USERNAME", "")
    ADMINS: List[int] = [int(i) for i in os.getenv("ADMINS", "").split(",") if i.strip().isdigit()]
    NOTIFICATION_CHATS: List[int] = [
        int(x) for x in os.getenv("NOTIFICATION_CHATS", "")
        .replace("[", "").replace("]", "").split(",") if x.strip().isdigit()
    ]

settings = Settings()

# Backward compatibility (import qilinsa xatolik chiqmasin)
BOT_TOKEN = settings.BOT_TOKEN
TOKEN = settings.BOT_TOKEN
MONGO_URI = settings.MONGO_URI
OPENAI_API_KEY = settings.OPENAI_API_KEY
REDIS_URI = settings.REDIS_URI
MONGO_DB_NAME = settings.MONGO_DB_NAME
LOG_LEVEL = settings.LOG_LEVEL
DAILY_NOTIFICATION_TIME = settings.DAILY_NOTIFICATION_TIME
MEDIA_CHANNEL_ID = settings.MEDIA_CHANNEL_ID
MEDIA_CHANNEL_USERNAME = settings.MEDIA_CHANNEL_USERNAME
ADMINS = settings.ADMINS
NOTIFICATION_CHATS = settings.NOTIFICATION_CHATS

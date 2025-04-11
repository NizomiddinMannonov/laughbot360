# services/database.py

import logging
from pymongo import MongoClient
from config import MONGO_URI

# 📦 MongoDB ulanish
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client["laughbot360"]
    users_collection = db["users"]
    client.server_info()  # Trigger connection
    logging.info("✅ MongoDB successfully connected.")
except Exception as e:
    logging.error(f"❌ MongoDB bilan ulanishda xatolik: {e}")
    users_collection = None


# 🌐 Foydalanuvchining tanlangan tilini olish
def get_user_language(user_id: int) -> str | None:
    if users_collection is not None:
        user = users_collection.find_one({"user_id": user_id})
        if user and "language" in user:
            return user["language"]
    return None


# 🌐 Foydalanuvchi tanlagan tilni saqlash
def save_user_language(user_id: int, language_code: str) -> None:
    if users_collection is not None:
        users_collection.update_one(
            {"user_id": user_id},
            {"$set": {"language": language_code}},
            upsert=True
        )


# ⚠️ Barcha foydalanuvchilarni tozalash (faqat test vaqtida ishlatish tavsiya qilinadi!)
def clear_all_users() -> None:
    if users_collection is not None:
        logging.warning("🚨 CLEARING ALL USER DATA FROM MONGODB...")
        users_collection.delete_many({})
        logging.info("✅ Barcha foydalanuvchilar tozalandi.")

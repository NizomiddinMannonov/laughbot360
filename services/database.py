# 📁 services/database.py

import logging
from pymongo import MongoClient
from config import MONGO_URI
from bson import ObjectId
from datetime import datetime

# 📦 MongoDB ulanish
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client["laughbot360"]
    users_collection = db["users"]
    prompts_collection = db["prompts"]
    client.server_info()  # Trigger connection
    logging.info("✅ MongoDB successfully connected.")
except Exception as e:
    logging.error(f"❌ MongoDB bilan ulanishda xatolik: {e}")
    users_collection = None
    prompts_collection = None

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

# 🧠 Prompt saqlash

def save_prompt(prompt: str) -> str:
    if prompts_collection is not None:
        doc = {"prompt": prompt}
        result = prompts_collection.insert_one(doc)
        return str(result.inserted_id)
    return ""

# 🧠 Promptni ID orqali olish

def get_prompt_by_id(prompt_id: str) -> str | None:
    if prompts_collection is not None:
        doc = prompts_collection.find_one({"_id": ObjectId(prompt_id)})
        return doc["prompt"] if doc else None
    return None

# ⏳ Foydalanuvchi kunlik limitini tekshirish va yangilash

def check_user_daily_limit(db, user_id: int, daily_limit: int = 3) -> tuple[bool, int]:
    if db is not None:
        user = db.find_one({"user_id": user_id})
        today = datetime.utcnow().date()

        if not user:
            db.insert_one({"user_id": user_id, "date": today.isoformat(), "count": 1})
            return True, daily_limit - 1

        user_date = datetime.fromisoformat(user.get("date", today.isoformat())).date()
        count = user.get("count", 0)

        if user_date < today:
            db.update_one({"user_id": user_id}, {"$set": {"date": today.isoformat(), "count": 1}})
            return True, daily_limit - 1

        if count < daily_limit:
            db.update_one({"user_id": user_id}, {"$inc": {"count": 1}})
            return True, daily_limit - count - 1

        return False, 0

    return False, 0

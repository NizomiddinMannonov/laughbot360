import logging
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

logger = logging.getLogger(__name__)

mongo_client = AsyncIOMotorClient(settings.MONGO_URI)
db = mongo_client[settings.MONGO_DB_NAME]

users_collection = db['users']
memes_collection = db['memes']
likes_collection = db['meme_likes']

# --- DATABASE SETUP ---
async def setup_database() -> None:
    await users_collection.create_index('telegram_id', unique=True)
    await memes_collection.create_index('user_id')
    await likes_collection.create_index([('meme_id', 1), ('user_id', 1)], unique=True)
    logger.info("Database and indexes are set up.")

async def clear_all_users() -> None:
    """DEBUG uchun barcha user, mem va statistikani o‘chiradi."""
    await users_collection.delete_many({})
    await memes_collection.delete_many({})
    await likes_collection.delete_many({})
    logger.info("All users, memes and likes deleted.")

# --- USER MANAGEMENT ---
async def add_user(user_id: int, language: str = "en") -> None:
    await users_collection.update_one(
        {"telegram_id": user_id},
        {"$setOnInsert": {"telegram_id": user_id, "language": language}},
        upsert=True
    )

async def get_user(user_id: int) -> dict | None:
    return await users_collection.find_one({"telegram_id": user_id})

async def get_user_language(user_id: int) -> str:
    user = await get_user(user_id)
    return user.get("language", "en") if user else "en"

async def save_user_language(user_id: int, lang_code: str) -> None:
    await users_collection.update_one(
        {"telegram_id": user_id},
        {"$set": {"language": lang_code}},
        upsert=True
    )

# --- LIMIT CHECK ---
async def check_user_daily_limit(user_id: int, daily_limit: int = 3) -> tuple[bool, int]:
    start_of_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    memes_today = await memes_collection.count_documents({
        "user_id": user_id,
        "created_at": {"$gte": start_of_day}
    })
    remaining = max(0, daily_limit - memes_today)
    return (remaining > 0, remaining)

# --- PROMPT/MEME ---
async def save_prompt(prompt: str, user_id: int = None) -> str:
    doc = {
        "prompt": prompt,
        "user_id": user_id,
        "created_at": datetime.now()
    }
    result = await memes_collection.insert_one(doc)
    return str(result.inserted_id)

async def get_prompt_by_id(prompt_id: str) -> str | None:
    from bson import ObjectId
    doc = await memes_collection.find_one({"_id": ObjectId(prompt_id)})
    return doc.get("prompt") if doc else None

async def save_meme(user_id: int, file_id: str, caption: str, prompt: str = None, created_at=None) -> str:
    doc = {
        "user_id": user_id,
        "file_id": file_id,
        "caption": caption,
        "prompt": prompt,
        "created_at": created_at or datetime.now()
    }
    result = await memes_collection.insert_one(doc)
    return str(result.inserted_id)

async def get_meme_by_id(meme_id: str) -> dict | None:
    from bson import ObjectId
    return await memes_collection.find_one({"_id": ObjectId(meme_id)})

async def get_user_memes(user_id: int, limit: int = 5):
    cursor = memes_collection.find({"user_id": user_id, "file_id": {"$exists": True}}).sort("created_at", -1).limit(limit)
    return await cursor.to_list(length=limit)

# --- LIKE / DISLIKE ---
async def add_meme_vote(meme_id: str, user_id: int, vote: str):
    await likes_collection.update_one(
        {"meme_id": meme_id, "user_id": user_id},
        {"$set": {"vote": vote, "timestamp": datetime.now()}},
        upsert=True
    )

async def has_voted(meme_id: str, user_id: int):
    doc = await likes_collection.find_one({"meme_id": meme_id, "user_id": user_id})
    return doc['vote'] if doc else None

async def get_meme_stats(meme_id: str):
    like_count = await likes_collection.count_documents({"meme_id": meme_id, "vote": "like"})
    dislike_count = await likes_collection.count_documents({"meme_id": meme_id, "vote": "dislike"})
    return like_count, dislike_count

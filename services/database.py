# services/database.py

from pymongo import MongoClient
from os import getenv
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["laughbot360"]
users = db["users"]

def save_user_language(user_id: int, language_code: str):
    users.update_one(
        {"_id": user_id},
        {"$set": {"language": language_code}},
        upsert=True
    )

def get_user_language(user_id: int) -> str:
    user = users.find_one({"_id": user_id})
    return user.get("language", "uz") if user else "uz"

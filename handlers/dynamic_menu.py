# handlers/dynamic_menu.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Text

router = Router()

# Dinamik menyu: bu erda inline tugmalar bilan ham kiritish mumkin
# Misol uchun, foydalanuvchi "1️⃣" deb matn yuborsa, AI savol-javob moduliga yo‘naltiriladi.
@router.message(F.text.in_({"1️⃣", "2️⃣", "3️⃣"}))
async def menu_selection(message: Message):
    selection = message.text.strip()
    if selection == "1️⃣":
        await message.answer("AI Savol-Javob funksiyasi hozirda tayyorlanmoqda. Iltimos, keyinroq qaytadan urinib ko‘ring.")
        # Bu yerga services/ai_response.py modulidan funksiya chaqirilishi mumkin
    elif selection == "2️⃣":
        await message.answer("Mem yaratish funksiyasi hozirda tayyorlanmoqda. Iltimos, keyinroq qaytadan urinib ko‘ring.")
        # Bu yerda meme_generator moduliga o'tish jarayonini qo'shamiz
    elif selection == "3️⃣":
        await message.answer("Tilni o‘zgartirish funksiyasi hozirda tayyorlanmoqda. Iltimos, keyinroq qaytadan urinib ko‘ring.")
        # Lokalizatsiya modulini qo‘shimcha qilamiz
    else:
        await message.answer("Iltimos, menyuni to‘g‘ri tanlang!")

# Istalgan callback sorovlar uchun ham handler qo'shish mumkin.
@router.callback_query(Text(startswith="menu:"))
async def handle_menu_callback(callback: CallbackQuery):
    # Callback query uchun misol
    data = callback.data.split(":")[1]
    await callback.message.answer(f"Siz tanladingiz: {data}")
    await callback.answer()

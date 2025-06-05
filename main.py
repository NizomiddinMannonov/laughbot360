import logging
import sys
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from handlers import (
    start, language, language_callback, help, meme, smart_meme, history
)
from services.database import setup_database, clear_all_users

# --- Logging config ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

# --- Bot komandalarini o‘rnatish ---
async def set_default_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Start the bot"),
        BotCommand(command="/help", description="Show help"),
        BotCommand(command="/trendmeme", description="Get trending meme idea"),
        BotCommand(command="/myhistory", description="Show my meme history"),
        BotCommand(command="/settings", description="Settings"),
    ]
    await bot.set_my_commands(commands)

# --- Startup ---
async def on_startup(bot: Bot):
    try:
        await setup_database()
        await clear_all_users()  # Faqat test uchun! Prodda O‘CHIRING!
        await set_default_commands(bot)
        logging.info("Bot started successfully (database cleared).")
    except Exception as e:
        logging.critical(f"Startup error: {e}")
        sys.exit(1)

# --- Routerlarni registratsiya qilish ---
def register_all_handlers(dp: Dispatcher):
    dp.include_router(history.router)
    dp.include_router(start.router)
    dp.include_router(language.router)
    dp.include_router(language_callback.router)
    dp.include_router(help.router)
    dp.include_router(smart_meme.router)
    dp.include_router(meme.router)
    

# --- Shutdown ---
async def on_shutdown():
    logging.info("Shutting down bot...")

# --- Main ---
async def main():
    if not BOT_TOKEN:
        logging.critical("BOT_TOKEN yo‘q! .env yoki config.py ni tekshiring.")
        sys.exit(1)

    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())
    register_all_handlers(dp)

    await on_startup(bot)

    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.exception(f"Polling paytida xatolik: {e}")
    finally:
        await on_shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot to‘xtatildi (KeyboardInterrupt)")

from aiogram import Dispatcher

# Har bir fayldan router import qilinmoqda
from .start import router as start_router
from .language import router as language_router
from .meme import router as meme_router
from .language_callback import router as language_callback_router
# from .history import router as history_router
# from .feedback import router as feedback_router

def register_all_handlers(dp: Dispatcher):
    # Routerlar navbatma-navbat ulangan
    dp.include_router(start_router)
    dp.include_router(language_router)
    dp.include_router(meme_router)
    dp.include_router(language_callback_router)
    # dp.include_router(feedback_router)

from aiogram import Dispatcher
from .start import router as start_router
from .language import router as lang_router
from .language_callback import router as lang_callback_router
from .meme import router as meme_router
from .smart_meme import router as smart_meme_router

def register_all_handlers(dp: Dispatcher):
    dp.include_router(start_router)
    dp.include_router(lang_router)
    dp.include_router(lang_callback_router)
    dp.include_router(meme_router)
    dp.include_router(smart_meme_router)

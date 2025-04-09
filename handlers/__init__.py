# handlers/__init__.py

from .base import router as base_router
from .dynamic_menu import router as menu_router
from .ai import router as ai_router  # ⬅️ YANGI

def register_all_handlers(dp):
    dp.include_router(base_router)
    dp.include_router(menu_router)
    dp.include_router(ai_router)  # ⬅️ RO‘YXATGA QO‘SHILDI

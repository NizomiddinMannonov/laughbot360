# 📁 states/meme.py
from aiogram.fsm.state import State, StatesGroup

class MemeState(StatesGroup):
    waiting_for_text = State()
    generating_meme = State()
    waiting_for_photo = State()
    editing_photo = State()

from aiogram.fsm.state import StatesGroup, State

class SmartMemeStates(StatesGroup):
    waiting_for_caption = State()
    waiting_for_description = State()

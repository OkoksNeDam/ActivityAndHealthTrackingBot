from aiogram.fsm.state import State, StatesGroup


class Registration(StatesGroup):
    choosing_first_name = State()
    choosing_last_name = State()
    choosing_favorite_animal = State()

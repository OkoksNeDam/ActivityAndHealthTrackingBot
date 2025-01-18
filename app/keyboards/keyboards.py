from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.utils.utils import WorkoutType


async def get_workout_keyboard() -> InlineKeyboardMarkup:
    """
    Create a keyboard from a list of workout types.
    :return: created keyboard.
    """
    keyboard = InlineKeyboardBuilder()
    for workout_type in WorkoutType:
        keyboard.add(InlineKeyboardButton(text=workout_type.value, callback_data=f"workout_{workout_type.value}"))
    return keyboard.adjust(2).as_markup()

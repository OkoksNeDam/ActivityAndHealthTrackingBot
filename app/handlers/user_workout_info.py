from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from app.utils.utils import calc_calories_from_workout
from datetime import datetime

from app.database.requests import user_workout_info_requests

user_workout_info_router = Router()


@user_workout_info_router.message(Command("log_workout"))
async def set_log_workout(message: Message, command: CommandObject):
    workout_type, workout_duration = command.args.split(' ')
    workout_duration = float(workout_duration)
    n_calories_burned = calc_calories_from_workout(workout_type=workout_type, workout_duration=workout_duration)
    await message.answer(f"{workout_type} {workout_duration} минут - {n_calories_burned} ккал.\n"
                         f"Дополнительно: выпейте {200 * workout_duration / 30} мл воды.")
    await user_workout_info_requests.set_user_workout_info(tg_id=message.from_user.id,
                                                           workout_type=workout_type,
                                                           duration=workout_duration,
                                                           date=datetime.now())

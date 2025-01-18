from datetime import datetime

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.database.requests import user_health_status_requests, user_water_consumption_requests,\
    user_food_consumption_requests, user_workout_info_requests
from app.utils.utils import calc_water_intake, calc_calories_intake

check_progress_router = Router()


@check_progress_router.message(Command("check_progress"))
async def check_progress(message: Message):
    today_health_status_list = await user_health_status_requests.get_health_status(tg_id=message.from_user.id,
                                                                                   date=datetime.now())
    today_health_status_list = list(today_health_status_list)
    if not today_health_status_list:
        await message.answer("Для отображения того, сколько осталось для выполнения нормы, добавьте"
                             "актуальную информацию о здоровье с помощью команды /set_health_status")
    else:
        user_latest_health_status = today_health_status_list[-1]
        today_water_consumption = \
            await user_water_consumption_requests.get_total_water_consumption(tg_id=message.from_user.id,
                                                                              date=datetime.now())
        required_water_amount = calc_water_intake(weight=user_latest_health_status.weight,
                                                  activity_level=user_latest_health_status.activity_level,
                                                  city=user_latest_health_status.city)
        today_calories_consumption = await user_food_consumption_requests.get_calories_sum(tg_id=message.from_user.id,
                                                                                           date=datetime.now())
        today_calories_burned = await user_workout_info_requests.get_n_calories_burned(tg_id=message.from_user.id,
                                                                                       date=datetime.now())
        required_calories_amount = calc_calories_intake(weight=user_latest_health_status.weight,
                                                        height=user_latest_health_status.height,
                                                        age=user_latest_health_status.age)
        await message.answer(f"📊 Прогресс на сегодня:\n\n"
                             f"💧 Вода:\n"
                             f"- Выпито: {today_water_consumption} л.\n"
                             f"- Норма: {round(required_water_amount, 2)} л.\n\n"
                             f"🍫 Калории:\n"
                             f"- Потреблено: {today_calories_consumption} ккал.\n"
                             f"- Сожжено: {today_calories_burned} ккал.\n"
                             f"- Норма: {required_calories_amount} ккал.")

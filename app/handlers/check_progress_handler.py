from datetime import datetime

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.database.requests import user_main_info_requests, user_water_consumption_requests, \
    user_food_consumption_requests, user_workout_info_requests
from app.utils.utils import calc_water_intake, calc_calories_intake

check_progress_router = Router()


@check_progress_router.message(Command("check_progress"))
async def check_progress(message: Message):
    """
    Handler for check_progress command.
    """
    user_main_info_list = await user_main_info_requests.get_user_main_info(tg_id=message.from_user.id,
                                                                                date=datetime.now())
    # TODO: вместо if else добавить исключения
    user_main_info_list = list(user_main_info_list)
    if not user_main_info_list:
        await message.answer("❗ Для отображения прогресса добавьте актуальную информацию"
                             " о здоровье с помощью команды /set_profile")
    else:
        # Since the user could add several data in one day, we select the last added information.
        user_latest_health_status = user_main_info_list[-1]
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
                             f"- Норма: {round(required_water_amount)} л.\n\n"
                             f"🍫 Калории:\n"
                             f"- Потреблено: {today_calories_consumption} ккал.\n"
                             f"- Сожжено: {today_calories_burned} ккал.\n"
                             f"- Норма: {required_calories_amount} ккал.")

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from datetime import datetime
from app.utils.utils import calc_water_intake

from app.database.requests import user_water_consumption_requests
from app.database.requests import user_health_status_requests

water_consumption_router = Router()


@water_consumption_router.message(Command("log_water"))
async def log_water(message: Message, command: CommandObject):
    await user_water_consumption_requests.set_water_consumption(tg_id=message.from_user.id,
                                                                n_liters=float(command.args),
                                                                date=datetime.now())
    await message.answer("Данные были успешно сохранены, спасибо!")
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
        await message.answer(f"📊 Прогресс:"
                             f"\nВыпито: {today_water_consumption} л."
                             f"\nНорма: {round(required_water_amount, 2)} л.")

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

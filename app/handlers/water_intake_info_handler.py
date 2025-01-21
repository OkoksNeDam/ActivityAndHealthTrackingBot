import re
from datetime import datetime

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from app.database.requests import user_water_intake_requests

water_consumption_router = Router()


@water_consumption_router.message(Command("log_water"))
async def log_water(message: Message, command: CommandObject):
    """
    Handler for logging water consumption info.

    The value must be either int or float.
    """
    if re.match(r'^-?\d+(?:\.\d+)$', command.args) or command.args.isdigit():
        await user_water_intake_requests.set_water_consumption(tg_id=message.from_user.id,
                                                               n_liters=float(command.args),
                                                               date=datetime.now())
        await message.answer("🎆 Данные были успешно сохранены, спасибо!")

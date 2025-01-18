from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from app.utils.utils import get_calories_of
from datetime import datetime

from app.database.requests import user_food_consumption_requests

food_consumption_router = Router()


@food_consumption_router.message(Command("log_food"))
async def log_food(message: Message, command: CommandObject):
    product_name, n_grams_eaten = command.args.split(' ')
    n_grams_eaten = float(n_grams_eaten)
    product_calories = get_calories_of(product_name)
    n_calories_eaten = product_calories * n_grams_eaten / 100
    await message.answer(f"{product_name} - {product_calories} ккал на 100 г.\n"
                         f"Количество употребленных калорий: {n_calories_eaten} ккал.")
    await user_food_consumption_requests.set_food_consumption(tg_id=message.from_user.id,
                                                              food_name=product_name,
                                                              n_calories_consumed=n_calories_eaten,
                                                              date=datetime.now())
    await message.answer("Данные были успешно сохранены, спасибо!")

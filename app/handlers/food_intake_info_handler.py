import re

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from app.utils.utils import get_calories_of
from datetime import datetime

from app.database.requests import user_food_intake_requests

food_consumption_router = Router()


@food_consumption_router.message(Command("log_food"))
async def log_food(message: Message, command: CommandObject):
    """
    Handler for logging food consumption.

    Two values are specified as parameters:
    the name of the product and the number of grams eaten.
    """
    args = command.args.split(' ')
    product_name, n_grams_eaten = args
    if len(args) != 2 or (re.match(r'^-?\d+(?:\.\d+)$', n_grams_eaten) is None and not n_grams_eaten.isdigit()):
        return
    n_grams_eaten = float(n_grams_eaten)
    product_calories = get_calories_of(product_name)
    if not product_calories:
        await message.answer("😞 К сожалению, не удалось найти информацию для данного продукта :(")
        return
    n_calories_eaten = product_calories * n_grams_eaten / 100
    await message.answer(f"🍽️ {product_name} - {product_calories} ккал на 100 г.\n"
                         f"🍫 Количество употребленных калорий: {n_calories_eaten} ккал.")
    await user_food_intake_requests.set_food_consumption(tg_id=message.from_user.id,
                                                         food_name=product_name,
                                                         n_calories_consumed=n_calories_eaten,
                                                         date=datetime.now())
    await message.answer("🎆 Данные были успешно сохранены, спасибо!")

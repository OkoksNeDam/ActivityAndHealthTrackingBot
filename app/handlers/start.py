from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import app.database.requests as rq

start_router = Router()


@start_router.message(Command("start"))
async def cmd_start(message: Message):
    user = await rq.get_user_info(tg_id=message.from_user.id)
    if user:
        await message.answer(f"Приветствуем, {user.first_name}! Как дела?")
    else:
        await rq.set_user_info(tg_id=message.from_user.id, first_name=message.from_user.first_name,
                               last_name=message.from_user.last_name)
        await message.answer(f"Приветствуем! Вы были успешно зарегестрированы под именем"
                             f" {message.from_user.first_name} {message.from_user.last_name}.")
    
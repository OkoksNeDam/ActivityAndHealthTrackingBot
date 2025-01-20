from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from app.database.requests import user_personal_info_requests

start_router = Router()


@start_router.message(Command("start"))
async def cmd_start(message: Message):
    """
    Handler for the bot start event.
    """
    user = await user_personal_info_requests.get_user_personal_info(tg_id=message.from_user.id)
    if user:
        # If the user has already been registered, then we simply welcome him.
        await message.answer(f"🖐 Приветствуем, {user.first_name}! Как дела?")
    else:
        # If the user has not been registered, we register him using information from the tg account.
        await user_personal_info_requests.set_user_personal_info(tg_id=message.from_user.id,
                                                                 first_name=message.from_user.first_name,
                                                                 last_name=message.from_user.last_name)
        await message.answer(f"🖐 Приветствуем! Вы были успешно зарегестрированы под именем"
                             f" {message.from_user.first_name} {message.from_user.last_name or ''}.")
    
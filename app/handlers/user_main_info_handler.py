from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from app.states.states import UserMainInfoState
from app.database.requests import user_main_info_requests
from datetime import datetime
from aiogram import F

user_main_info_router = Router()


@user_main_info_router.message(Command("set_profile"))
async def set_profile(message: Message, state: FSMContext):
    """
    Handler for setting main user info.
    """
    await state.set_state(UserMainInfoState.choosing_weight)
    await state.update_data(tg_id=message.from_user.id)
    await message.answer('> Введите Ваш текущий вес (в кг):')


@user_main_info_router.message(UserMainInfoState.choosing_weight,
                               (F.text.regexp(r'^-?\d+(?:\.\d+)$') | F.text.isdigit()))
async def register_weight(message: Message, state: FSMContext):
    """
    Weight input handler.

    The value must be either int or float.
    """
    await state.update_data(weight=float(message.text))
    await state.set_state(UserMainInfoState.choosing_height)
    await message.answer('> Введите Ваш текущий рост (в см):')


@user_main_info_router.message(UserMainInfoState.choosing_height,
                               (F.text.regexp(r'^-?\d+(?:\.\d+)$') | F.text.isdigit()))
async def register_height(message: Message, state: FSMContext):
    """
    Height input handler.

    The value must be either int or float.
    """
    await state.update_data(height=float(message.text))
    await state.set_state(UserMainInfoState.choosing_age)
    await message.answer('> Введите Ваш текущий возраст:')


@user_main_info_router.message(UserMainInfoState.choosing_age, F.text.isdigit())
async def register_age(message: Message, state: FSMContext):
    """
    Age input handler.

    The value must be int.
    """
    await state.update_data(age=int(message.text))
    await state.set_state(UserMainInfoState.choosing_activity_level)
    await message.answer('> Сколько минут активности у Вас в день?')


@user_main_info_router.message(UserMainInfoState.choosing_activity_level, F.text.isdigit())
async def register_activity_level(message: Message, state: FSMContext):
    """
    Activity level inout handler.

    The value must be int.
    """
    await state.update_data(activity_level=int(message.text))
    await state.set_state(UserMainInfoState.choosing_city)
    await message.answer('> В каком городе вы находитесь на данный момент времени?')


@user_main_info_router.message(UserMainInfoState.choosing_city)
async def register_city(message: Message, state: FSMContext):
    """
    City input handler.
    """
    await state.update_data(city=message.text, date=datetime.now())
    user_health_status = await state.get_data()
    await user_main_info_requests.set_user_main_info(**user_health_status)
    await message.answer("🎆 Данные были успешно сохранены, спасибо!")
    await state.clear()

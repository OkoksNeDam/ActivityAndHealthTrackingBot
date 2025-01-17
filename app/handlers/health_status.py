from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from app.states.states import HealthStatusState
from app.database.requests import user_health_status_requests
from datetime import datetime

health_status_router = Router()


@health_status_router.message(Command("set_health_status"))
async def set_health_status(message: Message, state: FSMContext):
    await state.set_state(HealthStatusState.choosing_weight)
    await state.update_data(tg_id=message.from_user.id)
    await message.answer('Введите Ваш текущий вес (в кг):')


@health_status_router.message(HealthStatusState.choosing_weight)
async def register_weight(message: Message, state: FSMContext):
    await state.update_data(weight=float(message.text))
    await state.set_state(HealthStatusState.choosing_height)
    await message.answer('Введите Ваш текущий рост (в см):')


@health_status_router.message(HealthStatusState.choosing_height)
async def register_height(message: Message, state: FSMContext):
    await state.update_data(height=float(message.text))
    await state.set_state(HealthStatusState.choosing_age)
    await message.answer('Введите Ваш текущий возраст:')


@health_status_router.message(HealthStatusState.choosing_age)
async def register_age(message: Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await state.set_state(HealthStatusState.choosing_activity_level)
    await message.answer('Сколько минут активности у Вас в день?')


@health_status_router.message(HealthStatusState.choosing_activity_level)
async def register_activity_level(message: Message, state: FSMContext):
    await state.update_data(activity_level=float(message.text))
    await state.set_state(HealthStatusState.choosing_city)
    await message.answer('В каком городе вы находитесь на данный момент времени?')


@health_status_router.message(HealthStatusState.choosing_city)
async def register_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text, date=datetime.now())
    user_health_status = await state.get_data()
    await user_health_status_requests.set_health_status(**user_health_status)
    await message.answer("Данные были успешно сохранены, спасибо!")
    await state.clear()

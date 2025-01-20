from datetime import datetime

from aiogram import F
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from app.database.requests import user_workout_info_requests
from app.keyboards.keyboards import get_workout_keyboard
from app.states.states import WorkoutInfoState
from app.utils.utils import calc_burned_calories_from_workout, WorkoutType

user_workout_info_router = Router()


@user_workout_info_router.message(Command("log_workout"))
async def set_log_workout(message: Message, state: FSMContext):
    """
    Handler for the log_workout command.

    When entering this command, the user has the opportunity
    to select the type of workout, as well as enter its duration.
    """
    await state.set_state(WorkoutInfoState.choosing_workout_type)
    await state.update_data(tg_id=message.from_user.id)
    await message.answer('> Выберите тип тренировки:', reply_markup=await get_workout_keyboard())


@user_workout_info_router.callback_query(F.data.startswith('workout_'), WorkoutInfoState.choosing_workout_type)
async def choosing_workout_type(callback: CallbackQuery, state: FSMContext):
    """
    Handler for choosing workout type.

    Entering the type of training is carried out using the keyboard.
    """
    workout_type = callback.data.split('_')[1]
    await state.update_data(workout_type=WorkoutType(workout_type))
    await state.set_state(WorkoutInfoState.choosing_duration)
    await callback.message.answer('> Введите продолжительность тренировки в минутах:')


@user_workout_info_router.message(WorkoutInfoState.choosing_duration, F.text.isdigit())
async def choosing_workout_duration(message: Message, state: FSMContext):
    """
    Handler for choosing workout duration.

    The workout duration is entered using a message. The given duration must be of type int.
    """
    await state.update_data(duration=abs(int(message.text)))
    workout_data = await state.get_data()
    await state.clear()
    workout_type, workout_duration = workout_data['workout_type'], workout_data['duration']
    n_calories_burned = calc_burned_calories_from_workout(workout_type=workout_type, workout_duration=workout_duration)
    await message.answer(f"🏋️ Тренировка: {workout_type.value} {workout_duration} минут -- {n_calories_burned} ккал.\n"
                         f"❗ Дополнительно: выпейте {round(200 * workout_duration / 30)} мл воды.")
    await user_workout_info_requests.set_user_workout_info(tg_id=message.from_user.id,
                                                           workout_type=workout_type,
                                                           duration=workout_duration,
                                                           date=datetime.now())
    await message.answer("🎆 Данные были успешно сохранены, спасибо!")

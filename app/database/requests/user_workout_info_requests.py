from datetime import datetime

from sqlalchemy import select, extract

from app.database.models import UserWorkoutInfo
from app.database.models import async_session
from app.utils.utils import calc_calories_from_workout


async def set_user_workout_info(tg_id: int, workout_type: str, duration: float, date: datetime) -> None:
    async with async_session() as session:
        session.add(UserWorkoutInfo(tg_id=tg_id, workout_type=workout_type, duration=duration, date=date))
        await session.commit()


async def get_n_calories_burned(tg_id: int, date: datetime) -> float:
    async with async_session() as session:
        user_workout_info = await session.scalars(select(UserWorkoutInfo)
                                                  .where(UserWorkoutInfo.tg_id == tg_id)
                                                  .filter(extract('year', UserWorkoutInfo.date) == date.year)
                                                  .filter(extract('month', UserWorkoutInfo.date) == date.month)
                                                  .filter(extract('day', UserWorkoutInfo.date) == date.day))
        total_burned_calories = sum(map(lambda x:
                                        calc_calories_from_workout(workout_type=x.workout_type,
                                                                   workout_duration=x.duration), user_workout_info))
        return total_burned_calories

from datetime import datetime

from sqlalchemy import select, extract

from app.database.models.models import UserWorkoutInfo
from app.database.models.models import async_session
from app.utils.utils import calc_burned_calories_from_workout, WorkoutType


async def set_user_workout_info(tg_id: int, workout_type: WorkoutType, duration: int, date: datetime) -> None:
    """
    Add user workout info to table.
    :param tg_id: user's tg id.
    :param workout_type: workout type, selected by user.
    :param duration: duration of workout in minutes.
    :param date: date of workout.
    """
    async with async_session() as session:
        session.add(UserWorkoutInfo(tg_id=tg_id, workout_type=workout_type, duration=duration, date=date))
        await session.commit()


async def get_n_calories_burned(tg_id: int, date: datetime) -> float:
    """
    Get total amount of burned calories from table.
    :param tg_id: user's tg id.
    :param date: date of workouts.
    :return: sum of burned calories from selected date.
    """
    async with async_session() as session:
        user_workout_info = await session.scalars(select(UserWorkoutInfo)
                                                  .where(UserWorkoutInfo.tg_id == tg_id)
                                                  .filter(extract('year', UserWorkoutInfo.date) == date.year)
                                                  .filter(extract('month', UserWorkoutInfo.date) == date.month)
                                                  .filter(extract('day', UserWorkoutInfo.date) == date.day))
        total_burned_calories = sum(map(lambda x:
                                        calc_burned_calories_from_workout(workout_type=x.workout_type,
                                                                          workout_duration=x.duration),
                                        user_workout_info))
        return total_burned_calories

from typing import List

from sqlalchemy import select, func, extract

from app.database.models.models import async_session
from app.database.models.models import UserFoodIntake
from datetime import datetime


async def set_food_consumption(tg_id: int, food_name: str, n_calories_consumed: float, date: datetime) -> None:
    """
    Add info about food consumption.
    :param tg_id: user's tg id.
    :param food_name: name of eaten product.
    :param n_calories_consumed: amount of calories consumed from selected product.
    :param date: date of adding info.
    """
    async with async_session() as session:
        session.add(UserFoodIntake(tg_id=tg_id, food_name=food_name,
                                   n_calories_consumed=n_calories_consumed, date=date))
        await session.commit()


async def get_calories_sum(tg_id: int, date: datetime) -> float:
    """
    Get total sum of calories consumed on selected date.
    :param tg_id: user's tg id.
    :param date: date on which data is taken.
    :return: sum of calories consumed.
    """
    async with async_session() as session:
        water_consumption = await session.scalars(select(func.coalesce(func.sum(UserFoodIntake.n_calories_consumed), 0))
                                                  .where(UserFoodIntake.tg_id == tg_id)
                                                  .filter(extract('year', UserFoodIntake.date) == date.year)
                                                  .filter(extract('month', UserFoodIntake.date) == date.month)
                                                  .filter(extract('day', UserFoodIntake.date) == date.day))
        return water_consumption.first()


async def get_list_of_food_intake(tg_id: int) -> List[UserFoodIntake]:
    """
    Get all records for selected user.
    :param tg_id: user's tg id.
    :return: list of user food consumption records.
    """
    async with async_session() as session:
        return await session.scalars(select(UserFoodIntake)
                                     .where(UserFoodIntake.tg_id == tg_id)
                                     .order_by(UserFoodIntake.date))

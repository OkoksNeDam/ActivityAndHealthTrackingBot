from typing import List

from app.database.models.models import async_session
from sqlalchemy import select, extract
from app.database.models.models import UserMainInfo
from datetime import datetime


async def set_user_main_info(tg_id: int, weight: float, height: float, age: int,
                             activity_level: int, city: str, date: datetime):
    """
    Add user's main info to table.
    :param tg_id: user's tg id.
    :param weight: user's weight.
    :param height: user's height.
    :param age: user's age.
    :param activity_level: user's average activity level.
    :param city: user's current city.
    :param date: date of added actual info.
    """
    async with async_session() as session:
        session.add(UserMainInfo(tg_id=tg_id, weight=weight, height=height, age=age,
                                 activity_level=activity_level, city=city, date=date))
        await session.commit()


async def get_user_main_info(tg_id: int, date: datetime) -> List[UserMainInfo]:
    """
    Get user main info from table.
    :param tg_id: user's tg id.
    :param date: date on which the user information was added.
    :return: list of user info on selected date.
    There may be multiple values if the user updated the table several times in one day.
    """
    async with async_session() as session:
        return await session.scalars(select(UserMainInfo)
                                     .where(UserMainInfo.tg_id == tg_id)
                                     .filter(extract('year', UserMainInfo.date) == date.year)
                                     .filter(extract('month', UserMainInfo.date) == date.month)
                                     .filter(extract('day', UserMainInfo.date) == date.day)
                                     .order_by(UserMainInfo.date.asc()))

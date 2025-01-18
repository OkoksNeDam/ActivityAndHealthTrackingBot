from typing import List

from app.database.models.models import async_session
from sqlalchemy import select, extract
from app.database.models.models import UserHealthStatus
from datetime import datetime


async def set_health_status(tg_id: int, weight: float, height: float, age: int,
                            activity_level: float, city: str, date: datetime):
    async with async_session() as session:
        session.add(UserHealthStatus(tg_id=tg_id, weight=weight, height=height, age=age,
                                     activity_level=activity_level, city=city, date=date))
        await session.commit()


async def get_health_status(tg_id: int, date: datetime) -> List[UserHealthStatus]:
    async with async_session() as session:
        return await session.scalars(select(UserHealthStatus)
                                     .where(UserHealthStatus.tg_id == tg_id)
                                     .filter(extract('year', UserHealthStatus.date) == date.year)
                                     .filter(extract('month', UserHealthStatus.date) == date.month)
                                     .filter(extract('day', UserHealthStatus.date) == date.day)
                                     .order_by(UserHealthStatus.date.asc()))

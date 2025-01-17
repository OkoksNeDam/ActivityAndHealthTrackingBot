from sqlalchemy import select, extract

from app.database.models import async_session
from app.database.models import UserWaterConsumption
from datetime import datetime
from sqlalchemy.sql import func


async def set_water_consumption(tg_id: int, n_liters: float, date: datetime) -> None:
    async with async_session() as session:
        session.add(UserWaterConsumption(tg_id=tg_id, n_liters=n_liters, date=date))
        await session.commit()


async def get_total_water_consumption(tg_id: int, date: datetime) -> float:
    async with async_session() as session:
        return await session.scalars(select(func.sum(UserWaterConsumption.n_liters))
                                     .where(UserWaterConsumption.tg_id == tg_id)
                                     .filter(extract('year', UserWaterConsumption.date) == date.year)
                                     .filter(extract('month', UserWaterConsumption.date) == date.month)
                                     .filter(extract('day', UserWaterConsumption.date) == date.day))

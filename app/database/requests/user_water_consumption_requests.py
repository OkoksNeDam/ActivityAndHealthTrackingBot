from sqlalchemy import select, extract

from app.database.models.models import async_session
from app.database.models.models import UserWaterConsumption
from datetime import datetime
from sqlalchemy.sql import func


async def set_water_consumption(tg_id: int, n_liters: float, date: datetime) -> None:
    """
    Add new water consumption info to table.
    :param tg_id: user's tg id.
    :param n_liters: user's water consumption in liters.
    :param date: date of updating info.
    """
    async with async_session() as session:
        session.add(UserWaterConsumption(tg_id=tg_id, n_liters=n_liters, date=date))
        await session.commit()


async def get_total_water_consumption(tg_id: int, date: datetime) -> float:
    """
    Get total water consumption on selected date.
    :param tg_id: user's tg id.
    :param date: date of getting water consumption info.
    :return: total sum of water consumption for selected date.
    """
    async with async_session() as session:
        water_consumption = await session.scalars(select(func.sum(UserWaterConsumption.n_liters))
                                                  .where(UserWaterConsumption.tg_id == tg_id)
                                                  .filter(extract('year', UserWaterConsumption.date) == date.year)
                                                  .filter(extract('month', UserWaterConsumption.date) == date.month)
                                                  .filter(extract('day', UserWaterConsumption.date) == date.day))
        return water_consumption.first()

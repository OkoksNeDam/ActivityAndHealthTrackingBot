from sqlalchemy import select, func, extract

from app.database.models.models import async_session
from app.database.models.models import UserFoodConsumption
from datetime import datetime


async def set_food_consumption(tg_id: int, food_name: str, n_calories_consumed: float, date: datetime) -> None:
    async with async_session() as session:
        session.add(UserFoodConsumption(tg_id=tg_id, food_name=food_name,
                                        n_calories_consumed=n_calories_consumed, date=date))
        await session.commit()


async def get_calories_sum(tg_id: int, date: datetime) -> float:
    async with async_session() as session:
        water_consumption = await session.scalars(select(func.sum(UserFoodConsumption.n_calories_consumed))
                                                  .where(UserFoodConsumption.tg_id == tg_id)
                                                  .filter(extract('year', UserFoodConsumption.date) == date.year)
                                                  .filter(extract('month', UserFoodConsumption.date) == date.month)
                                                  .filter(extract('day', UserFoodConsumption.date) == date.day))
        return water_consumption.first()

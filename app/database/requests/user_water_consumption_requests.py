from app.database.models import async_session
from sqlalchemy import select, inspect
from app.database.models import UserWaterConsumption
from datetime import datetime


async def set_water_consumption(tg_id: int, n_liters: float, date: datetime):
    async with async_session() as session:
        session.add(UserWaterConsumption(tg_id=tg_id, n_liters=n_liters, date=date))
        await session.commit()
from app.database.models import async_session
from sqlalchemy import select, inspect
from app.database.models import UserHealthStatus
from datetime import datetime


async def set_health_status(tg_id: int, weight: float, height: float, age: int,
                            activity_level: float, city: str, date: datetime):
    async with async_session() as session:
        session.add(UserHealthStatus(tg_id=tg_id, weight=weight, height=height, age=age,
                                     activity_level=activity_level, city=city, date=date))
        await session.commit()

from app.database.models import async_session
from app.database.models import UserFoodConsumption
from datetime import datetime


async def set_food_consumption(tg_id: int, food_name: str, n_calories_consumed: float, date: datetime) -> None:
    async with async_session() as session:
        session.add(UserFoodConsumption(tg_id=tg_id,
                                        food_name=food_name,
                                        n_calories_consumed=n_calories_consumed,
                                        date=date))
        await session.commit()
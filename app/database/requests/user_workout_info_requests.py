from app.database.models import async_session
from app.database.models import UserWorkoutInfo
from datetime import datetime


async def set_user_workout_info(tg_id: int, workout_type: str, duration: float, date: datetime) -> None:
    async with async_session() as session:
        session.add(UserWorkoutInfo(tg_id=tg_id, workout_type=workout_type, duration=duration, date=date))
        await session.commit()

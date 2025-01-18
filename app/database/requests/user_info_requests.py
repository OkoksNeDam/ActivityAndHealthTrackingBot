from app.database.models.models import async_session
from sqlalchemy import select
from app.database.models.models import UserPersonalInfo


async def set_user_info(tg_id: int, first_name: str, last_name: str) -> None:
    async with async_session() as session:
        session.add(UserPersonalInfo(tg_id=tg_id, first_name=first_name, last_name=last_name))
        await session.commit()


async def get_user_info(tg_id: int) -> UserPersonalInfo:
    async with async_session() as session:
        return await session.scalar(select(UserPersonalInfo).where(UserPersonalInfo.tg_id == tg_id))

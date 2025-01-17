from app.database.models import async_session
from sqlalchemy import select
from app.database.models import UserInfo


async def set_user_info(tg_id: int, first_name: str, last_name: str) -> None:
    async with async_session() as session:
        session.add(UserInfo(tg_id=tg_id, first_name=first_name, last_name=last_name))
        await session.commit()


async def get_user_info(tg_id: int) -> UserInfo:
    async with async_session() as session:
        return await session.scalar(select(UserInfo).where(UserInfo.tg_id == tg_id))

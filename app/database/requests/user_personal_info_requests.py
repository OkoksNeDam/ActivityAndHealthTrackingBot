from app.database.models.models import async_session
from sqlalchemy import select
from app.database.models.models import UserPersonalInfo


async def set_user_personal_info(tg_id: int, first_name: str, last_name: str) -> None:
    """
    Set new user personal info.
    :param tg_id: user's personal telegram id.
    :param first_name: user's first name.
    :param last_name: user's last name.
    """
    async with async_session() as session:
        session.add(UserPersonalInfo(tg_id=tg_id, first_name=first_name, last_name=last_name))
        await session.commit()


async def get_user_personal_info(tg_id: int) -> UserPersonalInfo:
    """
    Getting user information using id in telegram.
    :param tg_id: user's personal telegram id.
    :return: instance of UserPersonalInfo class.
    """
    async with async_session() as session:
        return await session.scalar(select(UserPersonalInfo).where(UserPersonalInfo.tg_id == tg_id))

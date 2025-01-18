from sqlalchemy import BigInteger, String, Integer, Float, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from datetime import datetime

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class UserInfo(Base):
    __tablename__ = 'users_info'

    tg_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(25))
    last_name: Mapped[str] = mapped_column(String(25))


class UserHealthStatus(Base):
    __tablename__ = 'users_health_status'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    weight: Mapped[float] = mapped_column(Float())
    height: Mapped[float] = mapped_column(Float())
    age: Mapped[int] = mapped_column(Integer())
    activity_level: Mapped[float] = mapped_column(Float())
    city: Mapped[str] = mapped_column(String(40))
    date: Mapped[datetime] = mapped_column(DateTime())


class UserWaterConsumption(Base):
    __tablename__ = 'users_water_consumption'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    n_liters: Mapped[float] = mapped_column(Float())
    date: Mapped[datetime] = mapped_column(DateTime())


class UserFoodConsumption(Base):
    __tablename__ = 'users_food_consumption'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    food_name: Mapped[str] = mapped_column(String(20))
    n_calories_consumed: Mapped[float] = mapped_column(Float())
    date: Mapped[datetime] = mapped_column(DateTime())


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

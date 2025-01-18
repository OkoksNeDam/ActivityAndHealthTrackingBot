import asyncio
from aiogram import Bot, Dispatcher
from app.config import BOT_TOKEN
from app.database.models import async_main
from app.handlers.health_status import health_status_router
from app.handlers.start import start_router
from app.handlers.water_consumption import water_consumption_router
from app.handlers.food_consumption import food_consumption_router

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_routers(start_router,
                   health_status_router,
                   water_consumption_router,
                   food_consumption_router)


async def main():
    await async_main()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

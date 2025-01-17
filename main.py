import asyncio
from aiogram import Bot, Dispatcher
from app.config import BOT_TOKEN
from app.database.models import async_main
from app.handlers.start import start_router


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(start_router)


async def main():
    await async_main()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

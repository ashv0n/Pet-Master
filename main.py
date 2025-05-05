import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from bot.handlers import start, actions, my_profile, unknown, info
from database.main import init_db
from database.models.pet import Pet
from database.models.user import User


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    routers = [
        start.router,
        actions.router,
        my_profile.router,
        info.router,

        
        unknown.router,
    ]

    for router in routers:
        dp.include_router(router)


    await init_db()
    print("Database initialized successfully.")

    print("Bot initialized successfully.")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

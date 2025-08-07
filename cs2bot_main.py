import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from handlers.message_handlers import *
from utils.database import db


async def money_up():
    all_ids = db.get_all_user_ids()

    for user in all_ids:
        user = str(user)
        user = user.replace('(', '').replace(')', '').replace(',', '')
        user_money = db.get_user_money(user)

        if user_money < 0:
            user_money = 0

        if user_money < 30:
            if user_money + 10 <= 30:
                db.add_user_money(user, 10)
            else:
                db.add_user_money(user, 30 - user_money)

async def main():
    await dp.start_polling(bot, skip_updates=False)

if __name__ == '__main__':
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(money_up, trigger='cron', hour=0, minute=0)
    scheduler.start()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

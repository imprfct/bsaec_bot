import logging

from aiogram import Dispatcher

from data.config import admins
from datetime import datetime

async def on_startup_notify(dp: Dispatcher):
    for admin in admins:
        try:
            await dp.bot.send_message(admin, f"Бот был запущен. \n{datetime.now()}")

        except Exception as err:
            logging.exception(err)

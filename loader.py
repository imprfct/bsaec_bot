from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

import pymysql
# Подключение к БД
con = pymysql.connect(host="localhost",
                     user="root",
                     password="8Ez7ENzj",
                     db="bsaec_bot_db",
                     charset='utf8mb4',
                     cursorclass=pymysql.cursors.DictCursor)
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from data import config
import pymysql
import sqlite3
import asyncio

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML, connections_limit=50)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

event_loop = asyncio.get_event_loop()

# Подключение к БД
con = sqlite3.connect("bsaec.db")

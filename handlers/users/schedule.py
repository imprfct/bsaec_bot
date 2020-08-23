"""
Этот модуль предназначен для отправки расписания
по выбранной пользователем даты для его группы.

Схема работы:
    1. Пользователь вводит /schedule
    2. Просим выбрать дату из календаря
(*) 3. Просим выбрать группу?
    4. Отправляем пользователю его расписание
"""

from loader import bot, dp, FSMContext
from aiogram import types

from datetime import date
from telegram_bot_calendar import LSTEP
from keyboards.inline.calendar import Calendar

@dp.message_handler(commands='schedule')
async def start(message):
    calendar, step = Calendar(locale="rus", min_date=date(2020, 1, 1), max_date=date.today()).build()
    await bot.send_message(message.chat.id,
                           f"Select {LSTEP[step]}",
                           reply_markup=calendar)


@dp.callback_query_handler(Calendar.func())
async def inline_kb_answer_callback_handler(query):
    result, key, step = Calendar(locale="rus", min_date=date(2020, 1, 1), max_date=date.today()).process(query.data)

    if not result and key:
        await bot.edit_message_text(f"Select {LSTEP[step]}",
                                    query.message.chat.id,
                                    query.message.message_id,
                                    reply_markup=key)
    elif result:
        # result - 2020-05-27
        await bot.edit_message_text(f"⏳ Ищу расписание на {result}",
                                    query.message.chat.id,
                                    query.message.message_id)
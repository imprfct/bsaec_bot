"""
Этот модуль предназначен для отправки расписания
по выбранной пользователем даты для его группы.

Схема работы:
    1. Пользователь вводит /schedule
    2. Просим выбрать дату из календаря
    3. Отправляем пользователю его расписание
"""

from loader import bot, dp, FSMContext
from aiogram import types

from datetime import date, timedelta
from telegram_bot_calendar import LSTEP
from keyboards.inline.calendar import Calendar

from utils.db_api.common import get_student_group, schedule_saved_in_bd,\
                        get_mode_by_chat_id, student_registrated
from schedule_app.main import download_day_for_group
from schedule_app.conf import weekdays


@dp.message_handler(commands='schedule', state="*")
async def start(message):
    if student_registrated(message.chat.id) is False:
        await message.answer("😱 Вы еще не зарегистрированы!\n\nДля регистрации попробуйте /start")
        return
    
    calendar, step = Calendar(locale="rus", min_date=date(
        2020, 1, 1), max_date=date.today() + timedelta(days=3)).build()
    await bot.send_message(message.chat.id,
                           f"Выберите год",
                           reply_markup=calendar)


@dp.callback_query_handler(Calendar.func())
async def inline_kb_answer_callback_handler(query):
    result, key, step = Calendar(locale="rus", min_date=date(
        2020, 1, 1), max_date=date.today() + timedelta(days=3)).process(query.data)

    if not result and key:
        await bot.edit_message_text(f"Выберите месяц и день",
                                    query.message.chat.id,
                                    query.message.message_id,
                                    reply_markup=key)
    elif result:
        # result - 2020-05-27 - type - date (from datetime)
        await bot.edit_message_text(f"⏳ Ищу расписание на {result}",
                                    query.message.chat.id,
                                    query.message.message_id)
        chat_id = query.from_user.id
        group = get_student_group(chat_id)
        requested_date = result

        # Проверка, есть ли такое расписание в БД
        schedule = schedule_saved_in_bd(requested_date, group)

        # Если есть, то отправить расписание
        if schedule is not None:
            await bot.send_photo(chat_id=chat_id,
                                 photo=schedule,
                                 caption="")
        # Иначе - скачать и отправить
        else:
            # бух-отдел ("б") или строит. отдел ("c")
            mode = get_mode_by_chat_id(chat_id)
            day = requested_date.strftime("%d")  # день типа 01, 02 ... 31
            month = requested_date.strftime("%m")   # Месяц типа 01, 02 ... 12
            year = requested_date.strftime("%Y")  # Год
            # переводим название дня недели с анг. на русский
            weekday = weekdays[requested_date.strftime("%A")]

            if mode == "б":
                url = f"http://bgaek.by/{day}-{month}-{year}-{weekday}/"
                msg_sended = download_day_for_group(user_who_requested=chat_id,
                                    url=url, req_date=requested_date, group=group)
                
                if msg_sended is False:
                    await bot.send_message(chat_id=chat_id,
                                    text="На сайте нет расписания "\
                                    f"на {day}.{month}.{year}... 😅")
            elif mode == "с":
                url = f"http://bgaek.by/расписание-на-{day}-{month}-{year}-{weekday}"
                msg_sended = download_day_for_group(user_who_requested=chat_id, url=url,
                                            req_date=requested_date, group=group)
                if msg_sended is False:
                    await bot.send_message(chat_id=chat_id,
                                    text="На сайте нет расписания "\
                                    f"на {day}.{month}.{year}... 😅")
            else:
                await bot.send_message(chat_id=chat_id,
                                    text="Произошла ошибка. Попробуйте еще раз")

"""
Этот модуль предназначен для отправки расписания
по выбранной пользователем даты для его группы.

Схема работы:
    1. Пользователь вводит /schedule
    2. Просим пользователя выбрать режим работы
        (подробнее - keyboards.inline.select_mode_kb.py)
    2. Просим выбрать дату из календаря
    3. Отправляем пользователю его расписание
"""

from loader import bot, dp, FSMContext
from aiogram import types

from datetime import date, timedelta
from telegram_bot_calendar import LSTEP
from keyboards.inline.calendar import Calendar
from keyboards.inline.groups_kb import get_groups_kb
from keyboards.inline.select_mode_kb import select_mode_kb

from utils.db_api.common import get_student_group, schedule_saved_in_bd,\
                        get_mode_by_chat_id, student_registrated
from schedule_app.main import download_day_for_group, get_groups
from schedule_app.conf import weekdays
import data.groups_and_specialities as gs
from states.schedule import ScheduleStates


@dp.message_handler(commands='schedule', state="*")
async def schedule_step_1(message, state:FSMContext):
    if student_registrated(message.chat.id) is False:
        await message.answer("😱 Вы еще не зарегистрированы!\n\nДля регистрации попробуйте /start")
        return
    
    await bot.send_message(message.chat.id, "Выберите режим работы: ",
                            reply_markup=select_mode_kb)

    await ScheduleStates.waiting_for_mode.set()

    
@dp.callback_query_handler(state=ScheduleStates.waiting_for_mode)
async def schedule_step_2(query, state:FSMContext):
    calendar, step = Calendar(locale="rus", min_date=date(
        2020, 1, 1), max_date=date.today() + timedelta(days=3)).build()
    
    async with state.proxy() as data:
        data['mode'] = query.data
    
    await bot.edit_message_text(f"Выберите год",
                                query.message.chat.id,
                                query.message.message_id,
                                reply_markup=calendar)
    
    await ScheduleStates.waiting_for_date.set()


@dp.callback_query_handler(Calendar.func(), state=ScheduleStates.waiting_for_date)
async def schedule_step_3(query, state:FSMContext):
    result, key, step = Calendar(locale="rus", min_date=date(
        2020, 1, 1), max_date=date.today() + timedelta(days=3)).process(query.data)

    if not result and key:
        await bot.edit_message_text(f"Выберите месяц и день",
                                    query.message.chat.id,
                                    query.message.message_id,
                                    reply_markup=key)
    elif result:
        requested_date = result
        # бух-отдел ("б") или строит. отдел ("c")
        day = requested_date.strftime("%d")  # день типа 01, 02 ... 31
        month = requested_date.strftime("%m")   # Месяц типа 01, 02 ... 12
        year = requested_date.strftime("%Y")  # Год
        
        # переводим название дня недели с анг. на русский
        weekday = weekdays[requested_date.strftime("%A")]
        
        buh_url = f"http://bgaek.by/{day}-{month}-{year}-{weekday}/"
        str_url_1 = f"http://bgaek.by/расписание-на-{day}-{month}-{year}-{weekday}"
        str_url_2 = f"http://bgaek.by/{day}-{month}-{year}-{weekday}-2/"
        urls =  [buh_url, str_url_1, str_url_2]

        async with state.proxy() as data:
            data['date'] = result
            data['urls'] = urls
            mode = int(data['mode'])

        if mode == 0:
            """
            Если пользователь запросил расписание для своей группы, то
            скидывать ему список групп просто бессмысленно, поэтому пропускаем
            этот шаг
            """
            await bot.edit_message_text(f"⏳ Ищу расписание",
                                    query.message.chat.id,
                                    query.message.message_id)

            chat_id = query.from_user.id
            group = get_student_group(chat_id)
            # Проверка, есть ли такое расписание в БД
            schedule = schedule_saved_in_bd(requested_date, group)
            

            # Если есть, то отправить расписание
            if schedule is not None:
                datestr = requested_date.strftime("%d.%m.%Y")
                await bot.send_photo(chat_id=chat_id,
                                    photo=schedule,
                                    caption=f"📆 Расписание на {datestr} для {group} группы")

            else:
                msg_sended = download_day_for_group(user_who_requested=chat_id,
                                                urls=urls, req_date=requested_date, group=group)
                if msg_sended is False:
                    await bot.send_message(chat_id=chat_id,
                                    text="На сайте нет расписания "\
                                    f"на {day}.{month}.{year}... 😅")
            
            await state.finish()
        
        elif mode == 1:
            groups = get_groups([buh_url, str_url_1, str_url_2])
            if groups == list():
                await bot.edit_message_text(f"На сайте нет расписания на {str(result)} 😅",
                                query.message.chat.id,
                                query.message.message_id,
                                reply_markup=get_groups_kb(groups))
                await state.finish()
                return
            else:
                await bot.edit_message_text(f"Выберите группу",
                                query.message.chat.id,
                                query.message.message_id,
                                reply_markup=get_groups_kb(groups))
            
            await ScheduleStates.waiting_for_group.set()


@dp.callback_query_handler(state=ScheduleStates.waiting_for_group)
async def schedule_step_4(query, state:FSMContext):
    await bot.edit_message_text(f"⏳ Ищу расписание",
                                    query.message.chat.id,
                                    query.message.message_id)

    chat_id = query.from_user.id
    async with state.proxy() as data:
        requested_date = data['date']
        urls = data['urls']
        mode = int(data['mode'])

    if mode == 0:
        group = get_student_group(query.message.chat.id)  
    else:
        group = query.data
    
    day = requested_date.strftime("%d")  # день типа 01, 02 ... 31
    month = requested_date.strftime("%m")   # Месяц типа 01, 02 ... 12
    year = requested_date.strftime("%Y")  # Год

    # Проверка, есть ли такое расписание в БД
    schedule = schedule_saved_in_bd(requested_date, group)

    # Если есть, то отправить расписание
    if schedule is not None:
        await bot.send_photo(chat_id=chat_id,
                            photo=schedule,
                            caption="")

    else:
        msg_sended = download_day_for_group(user_who_requested=chat_id,
                                        urls=urls, req_date=requested_date, group=group)
        if msg_sended is False:
            await bot.send_message(chat_id=chat_id,
                            text="На сайте нет расписания "\
                            f"на {day}.{month}.{year}... 😅")
    
    await state.finish()
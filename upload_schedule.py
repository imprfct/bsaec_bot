"""
Этот модуль отвечает за публикацию расписания в БД,
а также отправления пользователям расписаний
"""

import os
import asyncio
import pymysql
from loader import bot, con
from data.config import admins, spam_account
from schedule_app.conf import folder_path
from utils.db_api.common import get_students_groups
from datetime import date


async def upload_and_send_schedule(path, method, file_attr, requested_from):
    """
    Функция для загрузки id файлов с сервера в БД, а также подготовка к
    последующей отправки пользователям

    args:
        1. path: str - Путь к файлу
        2. method: method/def/func - Метод для отправки медиа (send_photo - для фото)
        3. file_attr: str - то, что мы загружаем ("photo", "video")
        4. requested_from: int/None - Пользователь, который запросил расписание
    """
    
    with open(path, 'rb') as file:
        # Отправляем фото кому-то, чтобы загрузить фото на сервер телеграма
        msg = await method(spam_account[0], file, disable_notification=True)

        # Получаем file_id нашего файла с сервера телеграм
        if file_attr == 'photo':
            file_id = msg.photo[-1].file_id
        else:
            file_id = getattr(msg, file_attr).file_id

        try:
            # Загрузка файла в БД
            with con.cursor() as cursor:
                cursor.execute(
                    f"INSERT INTO `bsaec_bot_db`.`media` (`file_id`, `filename`) VALUES ('{file_id}', '{path}');")
            con.commit()    # Подтверждаем изменения
        except Exception as e:
            print(
                'Couldn\'t upload file at {}. Error is {}'.format(path, e))
        else:
            # Если появилось новое расписание на сайте
            if requested_from is None:
                await sendScheduleToGroups(path=path, photo_id=file_id)
            
            # Если у нас запросили расписание
            else:
                await sendScheduleToStudent(path=path, photo_id=file_id,
                                            requested_from=requested_from)


async def sendScheduleToGroups(path: str, photo_id: str):
    """
    Отправляем расписание по группам
    """
    
    filename = path.split("/")[-1]
    group = filename.split("_")[3].split(".")[0]

    date_list = filename.split("_")[:3]
    year = int(date_list[0])
    month = int(date_list[1])
    day = int(date_list[2])
    
    _date = date(year, month, day).strftime("%d.%m.%y")

    datestr = f"📆 Расписание на {_date} для {group} группы"

    groups_have_students = get_students_groups()

    for _group in groups_have_students:
        if _group == group:
            for user in groups_have_students[_group]:
                await bot.send_photo(chat_id=user,
                                     photo=photo_id,
                                     caption=datestr)


async def sendScheduleToStudent(path: str, photo_id: str, requested_from):
    """
    Отправляем расписание пользователю, который его запрашивал
    """

    filename = path.split("/")[-1]
    group = filename.split("_")[3].split(".")[0]

    date_list = filename.split("_")[:3]
    year = int(date_list[0])
    month = int(date_list[1])
    day = int(date_list[2])
    datestr = f"📆 Расписание на {day}.{month}.{year}"
    
    _date = date(year, month, day).strftime("%d.%m.%y")
    datestr = f"📆 Расписание на {_date} для {group} группы"
    
    await bot.send_photo(chat_id=requested_from,
                         photo=photo_id,
                         caption=datestr)


async def uploadMediaFiles(folder, method, file_attr):
    """
    Функция берет файлы из папки и загружает их все в БД

    Подробных комментариев нет - функция временно не используется
    """
    
    folder_path = folder
    for counter, filename in enumerate(os.listdir(folder_path)):
        if counter % 100 == 0 and counter != 0:
            await asyncio.sleep(10)

        if filename.startswith('.'):
            continue
        
        with open(os.path.join(folder_path, filename), 'rb') as file:
            msg = await method(spam_account[0], file, disable_notification=True)
            if file_attr == 'photo':
                file_id = msg.photo[-1].file_id
            else:
                file_id = getattr(msg, file_attr).file_id

            try:
                # Загрузка файла в БД
                with con.cursor() as cursor:
                    cursor.execute(
                        f"INSERT INTO `bsaec_bot_db`.`media` (`file_id`, `filename`) VALUES ('{file_id}', '{os.path.join(folder_path, filename)}');")
                con.commit()
            except Exception as e:
                print(
                    'Couldn\'t upload {}. Error is {}'.format(filename, e))
            else:
                print(
                    f'Successfully uploaded and saved to DB file {filename} with id {file_id}')

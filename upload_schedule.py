import os
import asyncio
import pymysql
from loader import bot, con
from data.config import admins
from schedule_app.conf import folder_path
from utils.db_api.common import get_students_groups


async def sendSchedule(path: str, photo_id: str):
    filename = path.split("/")[-1]
    group = filename.split("_")[3].split(".")[0]

    date_list = filename.split("_")[:3]
    year = date_list[0]
    month = date_list[1]
    day = date_list[2]
    datestr = f"📆 Расписание на {day}.{month}.{year} для {group} группы"
    
    groups_have_students = get_students_groups()

    for _group in groups_have_students:
        if _group == group:
            for user in groups_have_students[_group]:
                await bot.send_photo(chat_id=user,
                                    photo=photo_id,
                                    caption=datestr)


async def upload_and_send_schedule(path, method, file_attr):
    with open(path, 'rb') as file:
        msg = await method(admins[0], file, disable_notification=True)
        if file_attr == 'photo':
            file_id = msg.photo[-1].file_id
        else:
            file_id = getattr(msg, file_attr).file_id
        
        try:
            # Загрузка файла в БД
            with con.cursor() as cursor:
                cursor.execute(f"INSERT INTO `bsaec_bot_db`.`media` (`file_id`, `filename`) VALUES ('{file_id}', '{path}');")
            con.commit()
        except Exception as e:
            print(
                'Couldn\'t upload file at {}. Error is {}'.format(path, e))
        else:
            await sendSchedule(path=path, photo_id=file_id)
            

async def uploadMediaFiles(folder, method, file_attr):
    folder_path = folder
    for filename in os.listdir(folder_path):
        if filename.startswith('.'):
            continue

        with open(os.path.join(folder_path, filename), 'rb') as file:
            msg = await method(admins[0], file, disable_notification=True)
            if file_attr == 'photo':
                file_id = msg.photo[-1].file_id
            else:
                file_id = getattr(msg, file_attr).file_id
            
            try:
                # Загрузка файла в БД
                with con.cursor() as cursor:
                    cursor.execute(f"INSERT INTO `bsaec_bot_db`.`media` (`file_id`, `filename`) VALUES ('{file_id}', '{filename}');")
                con.commit()
            except Exception as e:
                print(
                    'Couldn\'t upload {}. Error is {}'.format(filename, e))
            else:
                print(
                    f'Successfully uploaded and saved to DB file {filename} with id {file_id}')

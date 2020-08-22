import os
import asyncio
import pymysql
from loader import bot, con
from data.config import admins
from schedule_app.conf import folder_path


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


loop = asyncio.get_event_loop()

tasks = [
    loop.create_task(uploadMediaFiles(folder_path, bot.send_photo, 'photo')),
]

wait_tasks = asyncio.wait(tasks)
loop.run_until_complete(wait_tasks)
loop.close()
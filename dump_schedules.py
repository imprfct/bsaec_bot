from keyboards.inline.calendar import MIN_DATE, MAX_DATE
from datetime import date, timedelta
from schedule_app.conf import weekdays
from schedule_app.main import parse_page
import logging
from schedule_app.parse import PageParser
import os
from data.config import img_path
from upload_schedule import uploadMediaFiles
from loader import bot
import asyncio
from utils.db_api.common import truncate_media_table


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

logging.info("Запуск")


def download_all_days_in_range(min_date=MIN_DATE, max_date=MAX_DATE):
    for single_date in daterange(min_date, max_date):
        weekday = weekdays[single_date.strftime("%A")]
        date_str = single_date.strftime("%d-%m-%Y")

        buh_url = f"http://bgaek.by/{date_str}-{weekday}/"
        str_url_1 = f"http://bgaek.by/расписание-на-{date_str}-{weekday}"
        str_url_2 = f"http://bgaek.by/{date_str}-{weekday}-2/"

        urls = [buh_url, str_url_1, str_url_2]
        path_date_str = single_date.strftime("%Y_%m_%d")
        path = os.path.join(img_path, path_date_str)

        for url in urls:
            try:
                parse_page(url, path)
            except Exception:
                continue
        
        logging.info(f"Расписание на {date_str} скачано")
    
    return True


def add_in_db():
    asyncio.ensure_future(uploadMediaFiles(img_path, bot.send_photo, 'photo'), loop=asyncio.get_event_loop())

def upload_schedules():
    loop = asyncio.get_event_loop()

    tasks = [
        loop.create_task(uploadMediaFiles(img_path, bot.send_photo, 'photo')),
    ]

    wait_tasks = asyncio.wait(tasks)
    loop.run_until_complete(wait_tasks)
    loop.close()

if __name__ == "__main__":
    if truncate_media_table:
        if download_all_days_in_range():
            loop = asyncio.get_event_loop()

            tasks = [
                loop.create_task(uploadMediaFiles(img_path, bot.send_photo, 'photo')),
            ]

            wait_tasks = asyncio.wait(tasks)
            loop.run_until_complete(wait_tasks)
            loop.close()

            
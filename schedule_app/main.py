from . import conf  # Файл настроек для данной программы
from . import parse  # Мой модуль для парснга HTML-страниц с расписанием БГАЭК
from . import dfToImage    # Модуль для преобразования датафрейма в картинку
from data.config import img_path

import logging
import os
from datetime import datetime, timedelta, date   # Модуль для работы с датой
from bs4 import BeautifulSoup  # Класс для парсинга
from requests import get 	# Получение кода страницы из интернета
from time import sleep  # Функция для создания задержки


def parse_page(_url, _path):
    """
    Функция для получения расписания со страницы БГАЭК'а
    :param _url: URL страницы, которую хотим скачать
    :param _path: Путь, куда будут сохранены файлы с расписанием
    """
    parser = parse.PageParser(
        _url)  # Создаем объект типа Parser из модуля parse

    groups = parser.get_groups()  # Получаем все группы со страницы, которую нам передали
    # Получаем все расписания со страницы, которую нам передали
    schedules = parser.get_schedule()

    # Создаем все необходимые папки по пути, который нам передали аргументом
    os.makedirs(img_path, exist_ok=True)

    # Попарно перебираем все группы и расписания
    for group, schedule in zip(groups, schedules):
        if os.path.exists(f"{_path}_{group}.jpg"):
            continue
        else:
            dfToImage.get_image(schedule, path=f"{_path}_{group}",
                                requested_from=None)


def download_day(dates_and_links, year, month, day):
    """
    Функция, которая скачивает расписание по запросу
    В случае, если расписание не найдено, то функция ничего не возвращает
    Иначе она скачивает расписание по заданному пути
    """
    # Задаем путь!
    # Пример - 'Расписание 2020/1/1'
    path = os.path.join(img_path, f"{year}_{month}_{day}")

    # Находим ссылку по имеющейся дате
    # У нас будет 2 ссылки - одна для бух.отдела и строит.отдела
    indexes = list()
    for i in range(len(dates_and_links['date'])):
        date = dates_and_links['date'][i]
        if date.day == int(day) and date.month == int(month) and date.year == int(year):
            indexes.append(i)

    if len(indexes) not in [1, 2]:
        return
    elif(len(indexes) == 1):
        # Условная ссылка для строительного отделения
        link1 = dates_and_links['href'][indexes[0]]
        # Парсим страницы все страницы из словаря
        parse_page(_url=link1, _path=path)
    else:
        # Условная ссылка для строительного отделения
        link1 = dates_and_links['href'][indexes[0]]
        # Условная ссылка для бухгалтерского отделения
        link2 = dates_and_links['href'][indexes[1]]

        # Парсим страницы все страницы из словаря
        parse_page(_url=link1, _path=path)
        # Парсим страницы все страницы из словаря
        parse_page(_url=link2, _path=path)


def get_days_dict(date_and_links):
    """
    Эта функция создает словарь следующего типа:
    {'Год1':
        'Месяц1': ['День1', 'День2'],
        'Месяц2': ['День1', 'День2']
     ...
    }
    Словарь будет использован для сравнения какие расписания мы уже скачали,
    а какие только предстоит скачать
    """

    date_and_links_days = dict()    # Создаем словарь, который потом вернем

    # Перебираем все даты в объекте с датами
    for date in date_and_links['date']:
        year = str(date.year)   # Получаем год
        month = str(date.month)  # Получаем месяц
        day = str(date.day)     # Получаем день

        # Наполняем словарь недостающими элементами
        if year not in date_and_links_days:
            date_and_links_days[year] = dict()

        if month not in date_and_links_days[year]:
            date_and_links_days[year][month] = list()

        if day not in date_and_links_days[year][month]:
            date_and_links_days[year][month].append(day)

    return date_and_links_days


def download_day_for_group(user_who_requested, urls, req_date: date, group):
    """
    Функция для скачивания расписания на запрошенный день для запрошенной группы.

    args:
        user_who_requested: int - Id чата с пользователем
        url: str - с какой страницы брать расписание для скачивания
        req_date: datetime.date - Дата, на которую мы ищем расписание
        group: str - группа студента, запросившего расписание
    """
    try:
        for url in urls:
            try:
                # Создаем объект типа Parser из модуля parse
                parser = parse.PageParser(url)
                groups = parser.get_groups()  # Получаем все группы со страницы, которую нам передали
                if group not in groups:
                    continue
                else:
                    # Получаем все расписания со страницы, которую нам передали
                    schedules = parser.get_schedule()
                    break
            except Exception:
                continue

        os.makedirs(img_path, exist_ok=True)
        # Попарно перебираем все группы и расписания
        for _group, schedule in zip(groups, schedules):
            if _group == group:
                day = req_date.day
                month = req_date.month
                year = req_date.year
                dfToImage.get_image(data=schedule,
                                    path=os.path.join(img_path, f"{year}_{month}_{day}_{group}"),
                                    requested_from=user_who_requested)
                print(os.path.join(img_path, f"{year}_{month}_{day}_{group}"))
                return True
    except Exception:
        return False


def download_schedule(previous_date_and_links: dict()):
    """
    Функция для скачивания расписания.
    
    Схема работы:
        1. Получаем ссылки, имеющиеся на домашних страницах корпусов
        2. Если прошлые ссылки отличаются от новых, то появилось новое расписание,
        сответственно запускает процесс загрузки расписания
    """
    # создания объекта для парсинга домашних страниц
    home_parser = parse.HomePagesParser()
    # Получаем даты и ссылки на страницы расписания по дням
    date_and_links = home_parser.get_date_and_links()
    preloaded_days = get_days_dict(date_and_links)

    # Проходим по всем датам в preloaded_days,
    # если предыдущий объект дата-ссылка отличается от нынешнего,
    # то очевидно, что что-то изменилось, поэтому скачиваем новое расписание
    for year in preloaded_days:
        for month in preloaded_days[year]:
            for day in preloaded_days[year][month]:
                if not os.path.exists(img_path):
                    os.makedirs(img_path, exist_ok=True)
                if previous_date_and_links != date_and_links:
                    download_day(date_and_links, year, month, day)

    return date_and_links


def get_groups(urls: list):
    try:
        groups = list()
        for url in urls:
            try:
                # Создаем объект типа Parser из модуля parse
                parser = parse.PageParser(url)
                for group in parser.get_groups():
                    groups.append(group)
            except Exception:
                continue

        return groups
    except Exception:
        return None


def start_schedule_app():
    """
    Функция для запуска парсера
    """
    logging.info("Парсер запущен")
    # Используется для проверки, появилось ли новое расписание
    previous_date_and_links = dict()

    while True:
        previous_date_and_links = download_schedule(previous_date_and_links)
        # Задержка в 30с. для того, чтобы не делать много запросов
        sleep(30)  

    return True


if __name__ == '__main__':
    start_schedule_app()

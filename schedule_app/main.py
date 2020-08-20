import config  # Файл настроек для данной программы
import parse  # Мой модуль для парснга HTML-страниц с расписанием БГАЭК
import dfToImage    # Модуль для преобразования датафрейма в картинку

from os import makedirs, path, listdir, getcwd  # Работа с папками
from datetime import datetime, timedelta   # Модуль для работы с датой
from bs4 import BeautifulSoup # Класс для парсинга
from requests import get 	# Получение кода страницы из интернета
from time import sleep  # Функция для создания задержки


def parse_page(_url, _path):
    """
    Функция для получения расписания со страницы БГАЭК'а
    :param _url: URL страницы, которую хотим скачать
    :param _path: Путь, куда будут сохранены файлы с расписанием
    """
    parser = parse.PageParser(_url)  # Создаем объект типа Parser из модуля parse

    groups = parser.get_groups()  # Получаем все группы со страницы, которую нам передали
    schedules = parser.get_schedule()  # Получаем все расписания со страницы, которую нам передали

    makedirs(_path, exist_ok=True)  # Создаем все необходимые папки по пути, который нам передали аргументом

    # Попарно перебираем все группы и расписания
    for group, schedule in zip(groups, schedules):
        dfToImage.get_image(schedule, path=_path+"/"+group)


def download_day(dates_and_links, year, month, day):
    """
    Функция, которая скачивает расписание по запросу
    В случае, если расписание не найдено, то функция ничего не возвращает
    Иначе она скачивает расписание по заданному пути
    """

    print(f"Начинаю загрузку расписания на {day}-{month}-{year}")
    # Пример - 'Расписание 2020/1/1'
    path = config.folder_name + " " + year + "/" + month + "/" + day
    
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
        parse_page(_url=link1, _path=path)  # Парсим страницы все страницы из словаря
        # Логируем результат
        print(f"Расписание на {day}-{month}-{year} успешно загружено")
    else:
        # Условная ссылка для строительного отделения
        link1 = dates_and_links['href'][indexes[0]]
        # Условная ссылка для бухгалтерского отделения
        link2 = dates_and_links['href'][indexes[1]]

        parse_page(_url=link1, _path=path)  # Парсим страницы все страницы из словаря
        parse_page(_url=link2, _path=path)  # Парсим страницы все страницы из словаря
        # Логируем результат
        print(f"Расписание на {day}-{month}-{year} успешно загружено")


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
        month = str(date.month) # Получаем месяц
        day = str(date.day)     # Получаем день

        # Наполняем словарь недостающими элементами
        if year not in date_and_links_days:
            date_and_links_days[year] = dict()
        
        if month not in date_and_links_days[year]:
            date_and_links_days[year][month] = list()
        
        if day not in date_and_links_days[year][month]:
            date_and_links_days[year][month].append(day)

    return date_and_links_days


def download_day_for_group(url, path, datestr, group):
    parser = parse.PageParser(url)  # Создаем объект типа Parser из модуля parse

    groups = parser.get_groups()  # Получаем все группы со страницы, которую нам передали
    schedules = parser.get_schedule()  # Получаем все расписания со страницы, которую нам передали
    
    makedirs(path, exist_ok=True)
    
    # Попарно перебираем все группы и расписания
    for _group, schedule in zip(groups, schedules):
        if _group == group:
            dfToImage.get_image(schedule, path=path+datestr+"_"+group)
            return True
    
    return False


def download_schedule():
    global previous_date_and_links

    home_parser = parse.HomePagesParser()  # создания объекта для парсинга домашних страниц
    date_and_links = home_parser.get_date_and_links()  # Получаем даты и ссылки на страницы расписания по дням
    preloaded_days = get_days_dict(date_and_links)
    folderName = getcwd() + "/" + config.folder_name

    # Проходим по всем датам в preloaded_days,
    # если предыдущий объект дата-ссылка отличается от нынешнего,
    # то очевидно, что что-то изменилось, поэтому скачиваем новое расписание
    for year in preloaded_days:
        for month in preloaded_days[year]:
            for day in preloaded_days[year][month]:
                if not path.exists(folderName + " " + year + "/" + month + "/" + day):
                    download_day(date_and_links, year, month, day)
                else:
                    if previous_date_and_links != date_and_links:
                        download_day(date_and_links, year, month, day)
                        previous_date_and_links = date_and_links
    


if __name__ == '__main__':
    print("Запуск парсера...")
    # Используется для проверки, появилось ли новое расписание
    previous_date_and_links = dict()

    while True:
        download_schedule()

        sleep(1) # Задержка в 1 с. для того, чтобы компьютер не делал много запросов
        
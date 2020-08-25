from . import conf  # Файл с настройками парсера

import requests  # Библиотека для обращения к серверу, в нашем случае за HTML-разметкой
import bs4 as bs  # Модуль для парсинга HTML
import pandas as pd  # Библиотка для работы с информацией в виде ДатаФреймов (DataFrame)
from datetime import datetime  # Модуль для работы с датой и временем


class PageParser:
    """
    Класс используется для парсинга отдельной страницы с одним расписанием
    Methods:
        init - конструктор класса
        get_mode - получает режим работы. Может быть равен Б или С, в зависимости от страницы. Бух. отдел или строит.
        get_schedule - получает список датафреймов, содержащих расписания для каждой группы
        get_groups - получает список со всеми названиями групп на странице
        drop_null - отбрасывает пустые датафреймы и пустые строки в них
    """

    def __init__(self, url):
        """
        Конструктор для класса PageParser
        :param url: страница, которая будет парситься с использованием этого класса
        """
        self.url = url

        # Создаем фейковые метаданные
        self.schedule = list()  # Создаем пустой список, который будет хранить в себе расписания по порядку
        # Получаем HTML-код от URL
        page = requests.get(url, headers=conf.headers).text

        # --- Парсинг страницы ---
        self.soup = bs.BeautifulSoup(page, features='lxml')  # Преобразуем HTML в объект BeautifulSoup
        self.table = self.soup.find('table')  # Находим на странице таблицу с расписанием
        self.rows = self.table.find_all('tr')  # В таблице находим все строки

        # Режим в котором работает программа, Б - парсинг отделения бухучета, С - парсинг строит. отделения
        self.mode = ""
        self.mode = self.get_mode()

        self.groups = list()  # Создаем пустой список groups, содержащий в себе группы по порядку

    def get_mode(self):
        """
        Метод, который определяет режим работы парсера. Это необходимо в связи с тем, что разметка для бух. отделения
        и для строительного отделения отличается.
        IN : self
        OUT : None
        """
        # Получаем информацию о том, для кого мы парсим
        # Выглядит или так https://wampi.ru/image/6Vyklqs или так https://wampi.ru/image/6VykpLY
        modes = self.soup.find_all(attrs={"class": "meta-category"})
        for mode in modes:
            self.mode = self.mode + mode.text  # Получаем строку со всеми специальностями со страницы

        # Если в этой строке встречается Бух.учет, то предполагаем, что парсим страницу с расписанием бух.учета
        if "Бухгалтерский учет, анализ и контроль" in self.mode:
            return "Б"
        # Иначе - строительный отдел
        else:
            return "С"

    def get_schedule(self):
        """
        Метод, возвращающий список датафреймов, содержащих расписания на конкретной странице
        IN: self
        OUT: list(DataFrame('РАСПИСАНИЕ 1'), DataFrame('РАСПИСАНИЕ 2'))
        """
        try:
            # Структуры для хранения расписаний, их 2, т.к. страница поделена на расписания 2 групп. Пример: (23-п, 24-п
            first_group = {' ': list(), 'Предмет': list(), 'Аудитория': list()}
            second_group = {' ': list(), 'Предмет': list(), 'Аудитория': list()}

            iterations = 0  # Счетчик проходов

            # --- Формирование датафреймов с расписаниями ---
            for row in self.rows:
                split_row = row.find_all('td')  # Делим строку по столбцам

                last_pass = (iterations == len(self.rows) - 1)  # Проверка не в последний ли раз мы проходим

                # В случае, если мы попадаем на строку вида -, Группа1, Группа2. Тут происходит сохранение информации
                if split_row[0].text == ' ' and len(split_row[1].text) != 0:
                    # Формируем из словарей объекты типа DataFrame
                    first_group_df = pd.DataFrame(first_group)
                    second_group_df = pd.DataFrame(second_group)

                    # Если первый датфрейм не пустой
                    if not first_group_df.empty:
                        first_group_df.index = first_group_df[' ']  # Изменяем индексы с [0,1,2...] на номер часа
                        del first_group_df[' ']  # Удаляем стобец с часами для избавления от повторяющегося столбца
                        self.schedule.append(first_group_df)  # Добавляем датафрейм в список расписаний

                    # Если второй датфрейм не пустой
                    if not second_group_df.empty:
                        second_group_df.index = second_group_df[' ']  # Изменяем индексы с [0,1,2...] на номер часа
                        del second_group_df[' ']  # Удаляем стобец с часами для избавления от повторяющегося столбца
                        self.schedule.append(second_group_df)  # Добавляем датафрейм в список расписаний

                    # Обновляем словари для следующей пары групп
                    first_group = {' ': list(), 'Предмет': list(), 'Аудитория': list()}
                    second_group = {' ': list(), 'Предмет': list(), 'Аудитория': list()}

                # В случае, если эта строка вида №ч, предмет1, ауд1, предмет2, ауд2
                elif len(split_row) == 5:
                    hour = split_row[0].text  # Получаем номер часа по очереди
                    first_group_subject = split_row[1].text  # Получаем предмет для 1 группы
                    first_group_auditorium = split_row[2].text  # Получаем аудиторию для 1 группы
                    second_group_subject = split_row[3].text  # Получаем предмет для 2 группы
                    second_group_auditorium = split_row[4].text  # Получаем аудиторию для 2 группы

                    # Наполняем словарь 1 группы данными из строки:
                    first_group[' '].append(hour)
                    first_group['Предмет'].append(first_group_subject)
                    first_group['Аудитория'].append(first_group_auditorium)

                    # Наполняем словарь 2 группы данными из строки:
                    second_group[' '].append(hour)
                    second_group['Предмет'].append(second_group_subject)
                    second_group['Аудитория'].append(second_group_auditorium)

                # Обычно 6 столбцов появляются в случае, если у группы есть практика (как на скриншоте ниже)
                # https://wampi.ru/image/6VH9zWP
                elif len(split_row) == 6:
                    # Если ширина 2 столбца больше 3-его, то предполагаем, что практика на странице справа
                    if split_row[1].get("width") > split_row[2].get("width"):
                        hour = split_row[0].text  # Получаем номер часа по очереди
                        first_group_subject = split_row[1].text + " / " + split_row[2].text  # Предмет для 1 группы
                        first_group_auditorium = split_row[3].text  # Получаем аудиторию для 1 группы
                        second_group_subject = split_row[4].textt  # Предмет для 2 группы
                        second_group_auditorium = split_row[5].text  # Получаем аудиторию для 2 группы

                        # Наполняем словарь 1 группы данными из строки:
                        first_group[' '].append(hour)
                        first_group['Предмет'].append(first_group_subject)
                        first_group['Аудитория'].append(first_group_auditorium)

                        # Наполняем словарь 2 группы данными из строки:
                        second_group[' '].append(hour)
                        second_group['Предмет'].append(second_group_subject)
                        second_group['Аудитория'].append(second_group_auditorium)

                    # Иначе предполагаем, что практика на странице слева
                    else:
                        hour = split_row[0].text  # Получаем номер часа по очереди
                        first_group_subject = split_row[1].text  # Получаем предмет для 1 группы
                        first_group_auditorium = split_row[2].text  # Получаем аудиторию для 1 группы
                        second_group_subject = split_row[3].text + " / " + split_row[4].text  # Получаем практики
                        second_group_auditorium = split_row[5].text  # Получаем аудиторию для 2 группы

                        # Наполняем словарь 1 группы данными из строки:
                        first_group[' '].append(hour)
                        first_group['Предмет'].append(first_group_subject)
                        first_group['Аудитория'].append(first_group_auditorium)

                        # Наполняем словарь 2 группы данными из строки:
                        second_group[' '].append(hour)
                        second_group['Предмет'].append(second_group_subject)
                        second_group['Аудитория'].append(second_group_auditorium)

                # В случае если на одной строке сразу 2 практики
                elif len(split_row) == 7:
                    hour = split_row[0].text  # Получаем номер часа по очереди
                    first_group_subject = split_row[1].text + " / " + split_row[2].text  # Получаем предмет для 1 группы
                    first_group_auditorium = split_row[3].text  # Получаем аудиторию для 1 группы
                    second_group_subject = split_row[4].text + " / " + split_row[5].text  # Предмет для 2 группы
                    second_group_auditorium = split_row[6].text  # Получаем аудиторию для 2 группы

                    # Наполняем словарь 1 группы данными из строки:
                    first_group[' '].append(hour)
                    first_group['Предмет'].append(first_group_subject)
                    first_group['Аудитория'].append(first_group_auditorium)

                    # Наполняем словарь 2 группы данными из строки:
                    second_group[' '].append(hour)
                    second_group['Предмет'].append(second_group_subject)
                    second_group['Аудитория'].append(second_group_auditorium)

                # Если проходимся в последний раз, то сохраняем последние 2 датафрейма
                if last_pass:
                    # Формируем из словарей объекты типа DataFrame
                    first_group_df = pd.DataFrame(first_group)
                    second_group_df = pd.DataFrame(second_group)

                    # Изменяем индексы строк на номер часа по порядку
                    first_group_df.index = first_group_df[' ']
                    del first_group_df[' ']
                    second_group_df.index = second_group_df[' ']
                    del second_group_df[' ']

                    # Добавляем получившиеся датафреймы в список schedule
                    self.schedule.append(first_group_df)
                    self.schedule.append(second_group_df)

                iterations += 1
        # [DEBUG] В случае ошибки, можно отследить что произошло и на какой странице
        except Exception as exc:
            print(exc.args[0] + self.url)

        self.drop_null()  # Выкидываем пустые датафреймы и пустые строки в датафреймах

        return self.schedule  # Возвращаем список всех расписаний по порядку

    def get_groups(self):
        """
        Метод, возвращающий список групп на конкретной странице
        IN: self
        OUT: list('ГРУППА1', 'ГРУППА2', ...)
        """
        # Если парсим страницу с расписанием для бух-учета
        if self.mode == "Б":
            # --- Формирование списка групп ---
            for i in range(len(self.rows) - 1):
                split_row = self.rows[i].find_all('td')  # Разбиваем строку на отдельные столбцы

                # Это необходимо в случае, если в разметке такая ошибка: https://wampi.ru/image/6VyjX4k
                # Т.е. пропущен номер часа
                next_split_row = self.rows[i + 1].find_all("td")  # Получаем столбцы следующей строки

                # Если попадаем на строку вида -, Группа1, Группа2 и в след. строке находится расписание
                if split_row[0].text in conf.empty_strings and next_split_row[0].text not in conf.empty_strings:
                    # Добавляем группу в список всех групп
                    if len(split_row[1].text) > 0 and split_row[1].text not in conf.empty_strings:
                        self.groups.append(split_row[1].text)
                    if len(split_row[2].text) > 0 and split_row[2].text not in conf.empty_strings:
                        self.groups.append(split_row[2].text)
            return self.groups  # Возвращаем список всех групп

        # Если парсим страницу с расписанием для строительного отделения
        elif self.mode == "С":
            # --- Формирование списка групп ---
            for i in range(len(self.rows) - 1):
                split_row = self.rows[i].find_all('td')  # Разбиваем строку на отдельные столбцы

                # Это необходимо в случае, если в разметке такая ошибка: https://wampi.ru/image/6VyjX4k
                # Т.е. пропущен номер часа
                next_split_row = self.rows[i + 1].find_all('td')  # Получаем столбцы следующей строки

                # Если попадаем на строку вида -, Группа1, Кабинет1, Группа2, Кабинет2 и в следующей строке находится
                # расписание
                if split_row[0].text in conf.empty_strings and next_split_row[0].text not in conf.empty_strings:
                    # Добавляем группу в список всех групп в формате без номера курса
                    if len(split_row[1].text) > 0 and split_row[1].text not in conf.empty_strings:
                        self.groups.append(split_row[1].text.split(' ')[0])
                    if len(split_row[3].text) > 0 and split_row[3].text not in conf.empty_strings:
                        self.groups.append(split_row[3].text.split(' ')[0])

            return self.groups  # Возвращаем список всех групп

    def drop_null(self):
        """
        Метод для:
            удаления всех пустых строк в датафрейме,
            Удаления пустых групп (т.е. с названием типа "" или " ")
            Удаления все пустых датафреймов
        In: Self
        """

        # Удаляем группы с пустыми названиями
        for group in self.groups:
            if group in conf.empty_strings:
                self.groups.remove(group)

        # Удаляем пустые строки в датафреймах
        for schedule in self.schedule:
            # Перебираем все предметы и индексы строк
            for subject, hour, auditory in zip(schedule["Предмет"], schedule.index, schedule["Аудитория"]):
                # Если длина строки меньше или равна двойки, то в ней нет данных.
                if len(subject) <= 2 or (subject == "  /  ") \
                    or (subject in conf.empty_strings) or ("———" in subject) or ("___" in subject):

                    if len(auditory) >= 2:
                        continue

                    schedule.drop([hour], inplace=True)  # Удаляем строку из датафрейма

        # Удаляем разрывы строк в расписниях
        for schedule in self.schedule:
            for i in range(len(schedule["Предмет"]) - 1):
                if "\n" in schedule["Предмет"][i]:
                    schedule["Предмет"][i] = schedule["Предмет"][i].replace("\n", "")

        # Удалить все пустые датафреймы
        for i in range(len(self.schedule) - 1):
            try:
                if self.schedule[i].empty:
                    self.schedule.pop(i)
                
                if len(self.schedule[i].index) == 0:
                    self.schedule.pop(i)
            except IndexError:
                """
                Такое случается в случае, если на странице небольшая проблема с разметкой,
                Пропуская ошибку, мы не влияем на ход программы и результат 
                """
                continue


class HomePagesParser:
    """
    Класс используется для парсинга страниц, на которых находится по 10 расписаний.
    Methods:
       init - конструктор класса
       get_date_and_links - получить словарь с датой и ссылками на страницы с расписанием
       page_updates - если на странице поялвилось след. расписание - вернет True, иначе - False
    """

    def __init__(self):
        """
        Конструктор для класса HomePagesParser
        """

        self.urls = conf.urls  # Добавляем в класс поле urls для хранения ссылок, которые нам передали
        self.content = {"date": [], "href": []}  # Структура для хранения дат расписаний и ссылки на расписания
        self.content = self.get_date_and_links()  # При создании получаем эту структуру заполненной

    def get_date_and_links(self):
        """ Метод для получения словаря с ключами 'дата' и 'ссылка', дата указывает на какую дату ведет ссылка
            In: self
            OUT: dict("date": ["Дата1", "Дата2"], "href" : ["Ссылка1", "Ссылка2"])
        """
        dates_and_links = {"date": [], "href": []}  # Структура для хранения дат расписаний и ссылки на расписания
        # Перебираем все ссылки среди тех, которые нам передали
        for url in self.urls:
            with requests.get(url, headers=conf.headers) as page:
                soup = bs.BeautifulSoup(page.text, features='lxml')  # Формируем объект BeautifulSoup

                articles = soup.find_all('article')  # Находим все тэги с расписаниями
                
                # Перебираем все расписания
                for article in articles:
                    split_a = article.find("a").text.split(" ")  # Делим строку для удобства
                    if "buh-otdel" in page.url:  # Если парсим страницу бух.отдела
                        try:
                            dates_and_links["date"].append((datetime.strptime(split_a[0], "%d.%m.%Y")))
                        except IndexError:
                            print("На странице " + url + " обнаружена ошибка в разметке. Ошибка содержится в дне, "
                                                         "который был добавлен "
                                  + article.find("time").text + ". В качестве дня будет использоваться первый элемент")
                            dates_and_links["date"].append((datetime.strptime(split_a[0], "%d.%m.%Y")))

                    elif "stroi-otdel" in page.url:  # Если парсим страницу стр.отдела
                        try:
                            dates_and_links["date"].append((datetime.strptime(split_a[2], "%d.%m.%Y")))
                        except IndexError:
                            dates_and_links["date"].append((datetime.strptime(split_a[0], "%d.%m.%Y")))
                        except ValueError:
                            # Пример такой ошибки строка - `Расписание на 11 июня 2020`
                            try:
                                dates_and_links["date"].append((datetime.strptime(split_a[2] + "." + 
                                                conf.monthes[split_a[3]] + "." + split_a[4], "%d.%B.%Y")))
                            except KeyError:
                                # Пример - Расписание занятий на 30.06.2020г. (вторник)
                                dates_and_links["date"].append(datetime.strptime(split_a[3][:-2], "%d.%m.%Y"))

                    dates_and_links["href"].append(article.find("a").get("href"))  # Добавляем ссылку на расписание

        return dates_and_links  # Возвращаем объект

    def page_updates(self):
        """
        Функция, предназначенная для проверки домашней страницы на изменения
        :return: True, если произошли изменения
                 False, в обратном случае
        """
        if self.content != self.get_date_and_links():
            self.content = self.get_date_and_links()
            return True
        else:
            return False

# Ссылка на страницу со всеми расписаниями бухгалтерского отдела
buh_URL = "http://bgaek.by/category/расписание/buh-otdel/"
# Ссылка на страницу со всеми расписаниями строительного отдела
str_URL = "http://bgaek.by/category/расписание/stroi-otdel/"

urls = [buh_URL, str_URL]  # Список для удобного перебора ссылок

# Все возможные пустые строки (за время написания выявлены только эти)
empty_strings = ["", " ", " ", "\xa0", '\xa0\n\xa0', " "]

from os import getcwd
# Путь, где находится wkhtmltoimage
path_wkthmltoimage = f'{getcwd()}/schedule_app/wkhtmltopdf/bin/wkhtmltoimage.exe'

folder_path= "./data/Schedule"
queries_folder_name = "Запросы"

weekdays = {
    'Monday':'понедельник',
    'Tuesday':'вторник',
    'Wednesday':'среда',
    'Thursday':'четверг',
    'Friday':'пятница',
    'Saturday':'суббота',
    'Sunday':'воскресенье'
}

# для получения английского эквивалента из русского слова
monthes = {
    "1": "Январь",
    "2": "Февраль",
    "3": "Март",
    "4": "Апрель",
    "5": "Май",
    "6": "Июнь",
    "7": "Июль",
    "8": "Август",
    "9": "Сентябрь",
    "10": "Октябрь",
    "11": "Ноябрь",
    "12": "Декабрь"
}

# Метаданные для обхода DDOS-блокировки
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

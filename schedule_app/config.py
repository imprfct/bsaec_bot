# Ссылка на страницу со всеми расписаниями бухгалтерского отдела
buh_URL = "http://bgaek.by/category/расписание/buh-otdel/"
# Ссылка на страницу со всеми расписаниями строительного отдела
str_URL = "http://bgaek.by/category/расписание/stroi-otdel/"

urls = [buh_URL, str_URL]  # Список для удобного перебора ссылок

# Все возможные пустые строки (за время написания выявлены только эти)
empty_strings = ["", " ", " ", "\xa0", '\xa0\n\xa0', " "]

from os import getcwd
# Путь, где находится wkhtmltoimage
path_wkthmltoimage = f'{getcwd()}/wkhtmltopdf/bin/wkhtmltoimage.exe'

folder_name = "Raspisanie"
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
    "января": "January",
    "февраля": "February",
    "марта": "March",
    "апреля": "April",
    "мая": "May",
    "июня": "June",
    "июля": "July",
    "августа": "August",
    "сентября": "September",
    "октября": "October",
    "ноября": "November",
    "декабря": "December"
}

# Метаданные для обхода DDOS-блокировки
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

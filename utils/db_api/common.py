"""
Часто используемые функции и методы для работы с БД 
"""

import os
from loader import con
from datetime import date
from data.config import img_path


def truncate_media_table():
    """
    Полноcmью очистить таблицу с media
    """
    cursor = con.cursor()
    cursor.execute("TRUNCATE TABLE `media`;")
        
    con.commit()
    return True


def student_registrated(chat_id: int):
    """
    Проверка, зарегистрирован ли пользователь, если
    зарегистрирован, то вернет True, иначе False
    """
    cursor = con.cursor()
    cursor.execute(f"SELECT * FROM students WHERE chat_id = {chat_id};")
    if cursor.fetchone() is not None:
        return True
    else:
        return False


def get_student_group(chat_id: int):
    """
    Получение группы учащегося из БД
    """
    cursor = con.cursor()
    cursor.execute(
        f"SELECT `group` from students WHERE chat_id = {chat_id};")

    result = cursor.fetchone()

    return result[0]


def get_students_groups():
    """
    Функция возвращает словарь с ключом группа, а в
    качестве значения список chat_id студентов в этой группе
    """
    result = dict()

    cursor = con.cursor()
    select_sql = "SELECT `chat_id`, `group` FROM students;"
    cursor.execute(select_sql)

    for row in cursor.fetchall():
        group = row['group']
        chat_id = row['chat_id']

        if group not in result:
            result[group] = list()

        result[group].append(chat_id)

    return result


def schedule_saved_in_bd(date: date, group: str):
    path_to_file = os.path.join(img_path, f"{date.year}_{date.month}_{date.day}_{group}.jpg")
    
    cursor = con.cursor()
    sql = f'SELECT * from `media` WHERE `filename` = "{path_to_file}";'
    cursor.execute(sql)
    response = cursor.fetchall()

    if response is None or response == list() or response == tuple():
        return None
    else:
        return response[-1][0]


def get_mode_by_chat_id(chat_id: str):
    cursor = con.cursor()
    cursor.execute(f"SELECT `specialization` FROM `students` WHERE `chat_id`='{chat_id}';")
    specialization = cursor.fetchone()['specialization']
    
    # Согласно специализациям, установленным в data/groups_and_specialities.py
    if specialization <= 1:
        return "б"
    elif specialization > 1:
        return "с"
    else:
        return None

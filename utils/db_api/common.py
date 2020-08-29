"""
Часто используемые функции и методы для работы с БД 
"""

import os
import pymysql
from loader import con
from datetime import date
from data.config import img_path


def student_registrated(chat_id: int):
    """
    Проверка, зарегистрирован ли пользователь, если
    зарегистрирован, то вернет True, иначе False
    """
    with con.cursor() as cursor:
        cursor.execute(f"SELECT * FROM students WHERE chat_id = {chat_id};")
        if cursor.fetchone() is not None:
            return True
        else:
            return False


def get_student_group(chat_id: int):
    """
    Получение группы учащегося из БД
    """
    with con.cursor() as cursor:
        cursor.execute(
            f"SELECT `group` from students WHERE chat_id = {chat_id};")

        result = cursor.fetchone()

        return result['group']


def get_students_groups():
    """
    Функция возвращает словарь с ключом группа, а в
    качестве значения список chat_id студентов в этой группе
    """
    result = dict()

    with con.cursor() as cursor:
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
    with con.cursor() as cursor:
        sql = f"SELECT `file_id` FROM `media` WHERE `filename` = '{path_to_file}'"
        cursor.execute(sql)
        response = cursor.fetchone()

        if response is None:
            return None
        else:
            return response['file_id']


def get_mode_by_chat_id(chat_id: str):
    with con.cursor() as cursor:
        cursor.execute(f"SELECT `specialization` FROM `students` WHERE `chat_id`='{chat_id}';")
        specialization = cursor.fetchone()['specialization']
    
    # Согласно специализациям, установленным в data/groups_and_specialities.py
    if specialization <= 1:
        return "б"
    elif specialization > 1:
        return "с"
    else:
        return None

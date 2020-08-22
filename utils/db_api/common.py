"""
Часто используемые функции и методы для работы с БД 
"""

import pymysql
from loader import con


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

        if cursor.fetchone() is None:
            return None

        return cursor.fetchone()['group']


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

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
    

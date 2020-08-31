"""
Модуль для осуществления изменения данных в БД
"""

import pymysql
from datetime import datetime

from loader import con
from .common import student_registrated


def get_student_regdate(chat_id: int):
    """
    Получение даты и времени регистрации пользователя
    """
    con.ping(reconnect=True)    # Проверяем живо ли соединение с БД
    with con.cursor() as cursor:
        cursor.execute(f"SELECT `regdate` from students WHERE chat_id = {chat_id};")
        result = cursor.fetchone()

        if result is None:
            return None
        
        return result
        


def edit_student_group(chat_id: int, firstname: str, surname: str, group: str, specialization: str, datetime: datetime):
    """
    Функция для регистрации пользователя в БД
    """
    try:
        con.ping(reconnect=True)    # Проверяем живо ли соединение с БД
        with con.cursor() as cursor:
            sql_reg = "INSERT INTO `bsaec_bot_db`.`students` "\
                "(`chat_id`, `firstname`, `surname`, `group`, `specialization`, `regdate`) "\
                f"VALUES('{chat_id}', '{firstname}', '{surname}', "\
                f"'{group}', '{specialization}', '{datetime}')"

            cursor.execute(sql_reg)
            con.commit()    # Подтверждаем внесенные изменения
            return True
    except pymysql.err.IntegrityError as exc:
        print(exc)
        return False
    except pymysql.err.DataError as exc:
        print(exc)
        return False
    except TypeError as exc:
        print(exc)
        return False

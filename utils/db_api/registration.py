"""
Модуль для осуществления регистрации пользователя в БД
"""

import pymysql
from datetime import datetime

from loader import con, bot
from .common import student_registrated


def registrate_student(chat_id: int, firstname: str, surname: str, group: str, specialization: str):
    """
    Функция для регистрации пользователя в БД
    """
    try:
        with con.cursor() as cursor:
            sql_reg = "INSERT INTO `bsaec_bot_db`.`students` "\
                "(`chat_id`, `firstname`, `surname`, `group`, `specialization`, `regdate`) "\
                f"VALUES('{chat_id}', '{firstname}', '{surname}', "\
                f"'{group}', '{specialization}', '{datetime.now()}')"

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
    

"""
Этот модуль обслуживает команду /delete,
которая предназначена для удаления пользователя из БД
"""

from loader import con

def student_delete(chat_id: int):
    con.ping(reconnect=True)    # Проверяем живо ли соединение с БД
    with con.cursor() as cursor:
        cursor.execute(f"DELETE FROM students WHERE chat_id = {chat_id};")
        con.commit()
        return True
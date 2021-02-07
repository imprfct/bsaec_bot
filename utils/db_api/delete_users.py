"""
Этот модуль обслуживает команду /delete,
которая предназначена для удаления пользователя из БД
"""

from loader import con

def student_delete(chat_id: int):
    cursor = con.cursor()
    cursor.execute(f"DELETE FROM students WHERE chat_id = {chat_id};")
    con.commit()
    return True
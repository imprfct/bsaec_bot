"""
Этот модуль обслуживает команду /delete, которая предназначена
для удаления пользователя из БД

Схема работы:
1. Получаем сообщение /delete
2. Выполняем удаление (utils.db_api.delete_users - student_delete)
3. Уведомляем о ходе удаления
"""

from loader import dp
from aiogram import types
from utils.db_api.delete_users import student_delete
from utils.db_api.common import student_registrated


@dp.message_handler(commands=['delete'], state="*")
async def bot_delete_step_1(message: types.Message):
    if student_registrated(message.chat.id) is False:
        await message.answer("😱 Вы еще не зарегистрированы!\n\nДля регистрации попробуйте /start")
        return

    if student_delete(message.chat.id):
        await message.answer("✅ Вы были успешно удалены из системы!"\
            "\nСпасибо за использование ❤️")
    else:
        await message.answer("❌ Упс... Произошла непредвиденная ошибка. "\
                            "Попробуйте еще раз")

"""
Этот модуль обслуживает команду /delete, которая предназначена
для удаления пользователя из БД
"""

from loader import dp
from aiogram import types
from utils.db_api.delete_users import student_delete


@dp.message_handler(commands=['delete'], state="*")
async def bot_delete_step_1(message: types.Message):
    if student_delete(message.chat.id):
        await message.answer("✅ Вы были успешно удалены из системы! \nСпасибо за использование ❤️")
    else:
        await message.answer("❌ Упс... Произошла непредвиденная ошибка. Попробуйте еще раз")


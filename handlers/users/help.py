"""
Этот модуль обслуживает команду /help,
выдающую справку по боту.

Схема работы:
1. Получаем команду /help
2. Отправляем сообщение с возможными командами
"""

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp
from utils.misc import rate_limit


@rate_limit(5, 'help')
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = [
        'Список команд: ',
        '/start - Начать диалог',
        '/edit - Изменение группы',
        '/delete - Удаление себя из системы',
        '/help - Получить справку'
    ]
    await message.answer('\n'.join(text))

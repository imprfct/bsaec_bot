"""
В подобных файлах идет описание возможных состояний при 
выполнении какого-либо действия, подробнее и по-простому по ссылке ниже
https://mastergroosha.github.io/telegram-tutorial/docs/lesson_14/
"""

from aiogram.dispatcher.filters.state import State, StatesGroup

class Registration(StatesGroup):
    """
    Список того, что нужно сделать с пользователем при регистрации:
        1. Поприветствовать
        2. Запросить специальность
        3. Запросить группу в зависимоти от специальности
        4. Уведомить о ходе регистрации
    Первый и последний пункты всегда можно опустить, так как к ним доступ не нужен
    """
    waiting_for_specialization = State()
    waiting_for_group = State()
from aiogram.dispatcher.filters.state import State, StatesGroup

class ScheduleStates(StatesGroup):
    """
    Список того, что нужно сделать с пользователем при запросе расписания
        1. Предлагаем выбрать дату
        2. Предлагаем выбрать группу
    """
    waiting_for_date = State()
    waiting_for_group = State()
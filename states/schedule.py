from aiogram.dispatcher.filters.state import State, StatesGroup

class ScheduleStates(StatesGroup):
    """
    Список того, что нужно сделать с пользователем при запросе расписания
        1. Предлагаем выбрать режим работы (для своей или любой группы)
        2. Предлагаем выбрать дату
        3. Предлагаем выбрать группу
    """
    waiting_for_mode = State()
    waiting_for_date = State()
    waiting_for_group = State()
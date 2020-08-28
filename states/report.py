from aiogram.dispatcher.filters.state import State, StatesGroup

class ReportStates(StatesGroup):
    """
    Список того, что нужно сделать с пользователем при отправлении feedback
        1. Ожидаем текст и отправляем
    """
    waiting_for_message = State()

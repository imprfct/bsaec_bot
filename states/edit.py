from aiogram.dispatcher.filters.state import State, StatesGroup

class Edit(StatesGroup):
    """
    Список того, что нужно сделать с пользователем при изменении группы:
        1. Предложение выбрать новую специальность
        2. Предложение выбрать новую группу
    """
    waiting_for_specialization = State()
    waiting_for_group = State()
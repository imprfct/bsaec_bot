from data.groups_and_specialities import groups, specialities

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton
from math import ceil


"""
=== Клавиатура для выбора специальности ===
"""
spec_1 = KeyboardButton("Я учусь на бухгалтера 👨‍💼")
spec_2 = KeyboardButton("Я учусь на программиста 👨‍💻")
spec_3 = KeyboardButton("Я учусь на строителя 👷")
spec_4 = KeyboardButton("Я учусь на юриста 👨‍⚖️")
spec_5 = KeyboardButton("Я учусь на сантехника 👨‍🔧")

specializtion_kb = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)\
    .add(spec_1, spec_2).add(spec_3, spec_4).add(spec_5)


"""
=== Клавиатура для выбора группы ===

Данная клавиатура в отличии от прошлой является динамической и генерируется
прямо во время выполнения. Для корректной работы должен быть корректно заполнен
файлик groups_and_specialities.py в папке data 
"""


def get_groups_keyboard(speciality: str):
    if speciality not in specialities:
        return None

    specialities_have_groups = {
        "Бухгалтерский учет, анализ и контроль": list(),
        "Программное обеспечение информационных технологий": list(),
        "Промышленное и гражданское строительство": list(),
        "Правоведение": list(),
        "Санитарно-техническое обслуживание зданий и сооружений": list()
    }

    for group in groups:
        if "б" in group:
            specialities_have_groups["Бухгалтерский учет, анализ и контроль"].append(
                group)
        elif "п" in group:
            specialities_have_groups["Программное обеспечение информационных технологий"].append(
                group)
        elif "ю" in group:
            specialities_have_groups["Правоведение"].append(group)
        elif "ст" in group:
            specialities_have_groups["Санитарно-техническое обслуживание зданий и сооружений"].append(
                group)
        elif "с" in group:
            if "ст" in group:
                continue
            specialities_have_groups["Промышленное и гражданское строительство"].append(
                group)

    keyboard = ReplyKeyboardMarkup(
        one_time_keyboard=True, resize_keyboard=True, row_width=3)

    for group in specialities_have_groups[speciality]:
        keyboard.insert(group)

    return keyboard

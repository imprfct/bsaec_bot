"""
Этот модуль обслуживает команду старт и 
помогает зарегистрироваться любому пользователю

Схема работы:
1. Пользователь вводит /start
2. Приветсвуем пользователя
3. Запрашиваем специальность
4. Запрашиваем группу (в зависимоти от специальности)
5. Уведомить о ходе регистрации
"""

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, FSMContext
from utils.db_api import common, registration
from states.start import Registration

from keyboards.default import start_and_edit_kb
from data.groups_and_specialities import groups, encrypted_specialities


@dp.message_handler(CommandStart(), state="*")
async def bot_start_step_1(message: types.Message):
    chat_id = message.chat.id

    # Если пользователь уже зарегистрирован, то перерегистрация ему не нужна
    if common.student_registrated(chat_id) == True:
        await message.answer("Вы уже зарегистрированы ❤️", reply_markup=types.ReplyKeyboardRemove())

    else:
        await message.answer("Добро пожаловать 👋", reply_markup=types.ReplyKeyboardRemove())
        await message.answer("Выбери пожалуйста свою специальность:",
                             reply_markup=start_and_edit_kb.specializtion_kb)

        await Registration.waiting_for_specialization.set()


@dp.message_handler(state=Registration.waiting_for_specialization, content_types=types.ContentTypes.TEXT)
async def bot_start_step_2(message: types.Message, state: FSMContext):
    if message.text == "Я учусь на бухгалтера 👨‍💼":
        speciality = "Бухгалтерский учет, анализ и контроль"
        async with state.proxy() as data:
            data['specialization'] = speciality

        await message.answer("Выбери пожалуйста свою группу:",
                             reply_markup=start_and_edit_kb.get_groups_keyboard(speciality))
        await Registration.waiting_for_group.set()

    elif message.text == "Я учусь на программиста 👨‍💻":
        speciality = "Программное обеспечение информационных технологий"
        async with state.proxy() as data:
            data['specialization'] = speciality

        await message.answer("Выбери пожалуйста свою группу:",
                             reply_markup=start_and_edit_kb.get_groups_keyboard(speciality))
        await Registration.waiting_for_group.set()

    elif message.text == "Я учусь на строителя 👷":
        speciality = "Промышленное и гражданское строительство"
        async with state.proxy() as data:
            data['specialization'] = speciality

        await message.answer("Выбери пожалуйста свою группу:",
                             reply_markup=start_and_edit_kb.get_groups_keyboard(speciality))
        await Registration.waiting_for_group.set()

    elif message.text == "Я учусь на юриста 👨‍⚖️":
        speciality = "Правоведение"
        async with state.proxy() as data:
            data['specialization'] = speciality

        await message.answer("Выбери пожалуйста свою группу:",
                             reply_markup=start_and_edit_kb.get_groups_keyboard(speciality))
        await Registration.waiting_for_group.set()

    elif message.text == "Я учусь на сантехника 👨‍🔧":
        speciality = "Санитарно-техническое обслуживание зданий и сооружений"
        async with state.proxy() as data:
            data['specialization'] = speciality

        await message.answer("Выбери пожалуйста свою группу:",
                             reply_markup=start_and_edit_kb.get_groups_keyboard(speciality))
        await Registration.waiting_for_group.set()

    else:
        message.answer("Не очень вас понимаю, выберите пожалуйста из списка ниже: ",
                       reply_markup=start_and_edit_kb.specializtion_kb)


@dp.message_handler(state=Registration.waiting_for_group, content_types=types.ContentTypes.TEXT)
async def bot_start_step_3(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    firstname = message.chat.first_name
    surname = message.chat.last_name
    async with state.proxy() as data:
        speciality_text = data['specialization']
    speciality = encrypted_specialities[speciality_text]
    group = message.text

    # Если введенный текст не является группой
    if group not in groups:
        await message.answer("😕 Не могу понять. Выбери пожалуйста группу из списка ниже:",
                             reply_markup=start_and_edit_kb.get_groups_keyboard(speciality))

    if registration.registrate_student(chat_id=chat_id,
                                       firstname=firstname,
                                       surname=surname,
                                       group=group,
                                       specialization=speciality) == True:
        await message.answer("✅ Вы были успешно зарегистрированы!\n\nТеперь вы будете автоматические получать "\
                            "расписания. Для просмотра доступных команд введите /help",
                            reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("🤔 Что-то пошло не так... Попробуйте еще раз /start",\
                            reply_markup=types.ReplyKeyboardRemove())

    await state.finish()

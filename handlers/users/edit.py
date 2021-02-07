"""
Этот модуль обслуживает команду /edit,
которая предназначена для изменения группы.

Схема работы:
1. Пользователь вводит /edit
2. Предложение выбрать новую специальность
3. Предложение выбрать новую группу
4. Вывод информации о результате операции
"""

from loader import dp, FSMContext
from aiogram import types
from datetime import datetime

from states.edit import Edit
from utils.db_api.delete_users import student_delete
from keyboards.default import start_and_edit_kb

from data.groups_and_specialities import groups, encrypted_specialities
from utils.db_api import common, edit, delete_users
from utils.db_api.common import student_registrated


@dp.message_handler(commands=['edit'], state="*")
async def bot_edit_step_1(message: types.Message, state: FSMContext):
    if student_registrated(message.chat.id) is False:
        await message.answer("😱 Вы еще не зарегистрированы!\n\nДля регистрации попробуйте /start")
        return

    async with state.proxy() as data:
        if common.student_registrated(message.chat.id):
            if edit.get_student_regdate(message.chat.id) is not None:
                data['regdate'] = edit.get_student_regdate(message.chat.id)
                delete_users.student_delete(message.chat.id)
            else:
                await message.answer("Произошла ошибка!🤔 Попробуйте еще раз", reply_markup=types.ReplyKeyboardRemove())
                await state.finish()
                return

            await message.answer("Выбери пожалуйста свою специальность:",
                                 reply_markup=start_and_edit_kb.specializtion_kb)
            await Edit.waiting_for_specialization.set()
        else:
            await message.answer("Похоже, что вы не зарегистрированы.🤔 Пройдите регистрацию, введя команду /start",\
                                reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=Edit.waiting_for_specialization, content_types=types.ContentTypes.TEXT)
async def bot_edit_step_2(message: types.Message, state: FSMContext):
    if message.text == "Я учусь на бухгалтера 👨‍💼":
        speciality = "Бухгалтерский учет, анализ и контроль"
        async with state.proxy() as data:
            data['specialization'] = speciality

        await message.answer("Выбери пожалуйста свою группу:",
                             reply_markup=start_and_edit_kb.get_groups_keyboard(speciality))
        await Edit.waiting_for_group.set()

    elif message.text == "Я учусь на программиста 👨‍💻":
        speciality = "Программное обеспечение информационных технологий"
        async with state.proxy() as data:
            data['specialization'] = speciality

        await message.answer("Выбери пожалуйста свою группу:",
                             reply_markup=start_and_edit_kb.get_groups_keyboard(speciality))
        await Edit.waiting_for_group.set()

    elif message.text == "Я учусь на строителя 👷":
        speciality = "Промышленное и гражданское строительство"
        async with state.proxy() as data:
            data['specialization'] = speciality

        await message.answer("Выбери пожалуйста свою группу:",
                             reply_markup=start_and_edit_kb.get_groups_keyboard(speciality))
        await Edit.waiting_for_group.set()

    elif message.text == "Я учусь на юриста 👨‍⚖️":
        speciality = "Правоведение"
        async with state.proxy() as data:
            data['specialization'] = speciality

        await message.answer("Выбери пожалуйста свою группу:",
                             reply_markup=start_and_edit_kb.get_groups_keyboard(speciality))
        await Edit.waiting_for_group.set()

    elif message.text == "Я учусь на сантехника 👨‍🔧":
        speciality = "Санитарно-техническое обслуживание зданий и сооружений"
        async with state.proxy() as data:
            data['specialization'] = speciality

        await message.answer("Выбери пожалуйста свою группу:",
                             reply_markup=start_and_edit_kb.get_groups_keyboard(speciality))
        await Edit.waiting_for_group.set()

    else:
        message.answer("Не очень вас понимаю, выберите пожалуйста из списка ниже: ",
                       reply_markup=start_and_edit_kb.specializtion_kb)


@dp.message_handler(state=Edit.waiting_for_group, content_types=types.ContentTypes.TEXT)
async def bot_start_step_3(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    firstname = message.chat.first_name
    surname = message.chat.last_name
    async with state.proxy() as data:
        speciality_text = data['specialization']
        regdate = data['regdate'][0]
    speciality = encrypted_specialities[speciality_text]
    group = message.text

    # Если введенный текст не является группой
    if group not in groups:
        await message.answer("😕 Не могу понять. Выбери пожалуйста группу из списка ниже:",
                             reply_markup=start_and_edit_kb.get_groups_keyboard(speciality))

    if edit.edit_student_group(chat_id=chat_id,
                               firstname=firstname,
                               surname=surname,
                               group=group,
                               specialization=speciality,
                               datetime=regdate) == True:
        await message.answer("✅ Группа была успешно изменена",
                             reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("🤔 Что-то пошло не так... Попробуйте еще раз /start",
                             reply_markup=types.ReplyKeyboardRemove())

    await state.finish()

"""
Модуль обслуживает команду /report для отправки
и получения фидбэка от пользователей.

Принцип работы:
    1. Получаем команду /report
    2. Пересылаем сообщение администратору
    3. Когда администратор ответил на сообщение,
        пересылаем ответ запросившему
"""

from loader import dp, FSMContext, bot
from aiogram import types

from utils.db_api.common import student_registrated
from states.report import ReportStates
from data.config import admins

@dp.message_handler(commands=['report'], state="*")
async def bot_report_step_1(message: types.Message):
    if student_registrated(message.chat.id) is False:
        await message.answer("😱 Вы еще не зарегистрированы!\n\nДля регистрации попробуйте /start")
        return
    
    await message.answer("📝 Отправь мне сообщение и я отправлю его автору или введи `Отмена` (/cancel) для отмены")
    
    await ReportStates.waiting_for_message.set()
    

@dp.message_handler(state=ReportStates.waiting_for_message,
                    content_types=types.ContentTypes.PHOTO | types.ContentTypes.TEXT)
async def bot_report_step_2(message: types.Message, state: FSMContext):
    if message.text is not None:
        if message.text.lower() == "отмена" or message.text == "/cancel":
            await state.finish()
            await message.answer("Отправка сообщения отменена...")
            return
    
    for admin in admins:
        await message.forward(admin)
    
    await message.answer("💌 Ваше сообщение было успешно отправлено!")
    
    await state.finish()


"""
Если администратор осуществляет reply-ответ на пришедшее сообщение,
то отправляем ответ пользователю, из reply-сообщения
"""
@dp.message_handler(lambda message: message.reply_to_message and message is not None)
async def text_handler(message:types.Message):
    reply_msg = message.reply_to_message
    
    if reply_msg.forward_from is None:
        return
    
    chat_id = reply_msg.forward_from.id

    if str(message.chat.id) in admins:
        await bot.send_message(chat_id, f"Сообщение от администратора:\n\n{message.text}\n\nДля связи: @imperf3ct")
    
    await message.answer(f"Сообщение отправлено! 📤")
    
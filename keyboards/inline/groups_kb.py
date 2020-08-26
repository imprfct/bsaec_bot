from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


def get_groups_kb(groups: list):
    keyboard = InlineKeyboardMarkup(row_width=4)

    for group in groups:
        inline_btn = InlineKeyboardButton(text=group, callback_data=group)
        keyboard.insert(inline_btn)
    
    return keyboard
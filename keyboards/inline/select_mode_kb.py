from aiogram.types import InlineKeyboardMarkup,\
                            InlineKeyboardButton

select_mode_kb = InlineKeyboardMarkup()

my_group_btn = InlineKeyboardButton(text="Для своей группы", callback_data=0)
any_group_btn = InlineKeyboardButton(text="Для любой группы", callback_data=1)

select_mode_kb.add(my_group_btn).add(any_group_btn)
from telegram_bot_calendar import DetailedTelegramCalendar, MONTH, YEAR
from datetime import date

rus_translation_months = ["янв", "фев", "мар", "апр",
                        "май", "июн", "июл", "авг",
                        "сен", "окт", "ноя", "дек", ]

rus_translation_days_of_week = ['Пн', 'Вт', 'Ср',
                                'Чт', 'Пт', 'Сб', 'Вс']


class Calendar(DetailedTelegramCalendar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if date.today().year == self.min_date.year:
            self.first_step = MONTH
        else:
            self.first_step = YEAR

        self.size_month = 3

        self.empty_year_button = ""
        self.empty_month_button = ""
        self.empty_day_button = " "

        self.days_of_week['rus'] = rus_translation_days_of_week
        self.months['rus'] = rus_translation_months
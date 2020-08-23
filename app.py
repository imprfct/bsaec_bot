from schedule_app import main
from threading import Thread

async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)
    
    # Запуск процесса со скачиванием расписания
    schedule_app_thread = Thread(target=main.start_schedule_app)
    schedule_app_thread.start()

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)

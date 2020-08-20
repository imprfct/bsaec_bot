import asyncio
from oswatcher import watch_fs, WATCH_DIRECTORY


async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)
    
    # Запускаем процесс проверки наличия новых файлов в папке
    asyncio.get_running_loop().create_task(watch_fs(WATCH_DIRECTORY))
    
    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
"""
Этот модуль используется для того, чтобы включить `Наблюдатель`,
который будет следить за изменениями в папке. В случае нахождения нового файла
в папке с расписаниями, проверяем, расписание ли это и в случае успешной проверки,
отправляем его в нужную группу, подписывая правильной датой.
"""

import asyncio
from hachiko.hachiko import AIOWatchdog, AIOEventHandler

WATCH_DIRECTORY = './data'


class MyEventHandler(AIOEventHandler):
    """Subclass of asyncio-compatible event handler."""
    async def on_created(self, event):
        print('Created:', event.src_path)  # add your functionality here

    async def on_deleted(self, event):
        print('Deleted:', event.src_path)  # add your functionality here

    async def on_moved(self, event):
        print('Moved:', event.src_path)  # add your functionality here

    async def on_modified(self, event):
        print('Modified:', event.src_path)  # add your functionality here


async def watch_fs(watch_dir):
    evh = MyEventHandler()
    watch = AIOWatchdog(watch_dir, event_handler=evh)
    watch.start()
    for _ in range(20):
        await asyncio.sleep(1)
    watch.stop()
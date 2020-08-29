import imgkit
from .conf import path_wkthmltoimage
from sys import platform

from upload_schedule import upload_and_send_schedule
from loader import bot, event_loop
import asyncio

css = """<style type="text/css">
table.dataframe {
  font-family: Tahoma, Geneva, sans-serif;
  border: 0px solid #727272;
  text-align: left;
  border-collapse: collapse;
  width: 300px;
  height: 100%;
}
table.dataframe td, table.dataframe th {
  border: 1px solid #707070;
  padding: 5px 4px;
}
table.dataframe tbody td {
  font-size: 13px;
}
table.dataframe thead {
  background: #E0E0E0;
  background: -moz-linear-gradient(top, #e8e8e8 0%, #e3e3e3 66%, #E0E0E0 100%);
  background: -webkit-linear-gradient(top, #e8e8e8 0%, #e3e3e3 66%, #E0E0E0 100%);
  background: linear-gradient(to bottom, #e8e8e8 0%, #e3e3e3 66%, #E0E0E0 100%);
  border-bottom: 1px solid #000000;
}
table.dataframe thead th {
  font-size: 15px;
  font-weight: bold;
  color: #000000;
  text-align: center;
}
table.dataframe tfoot td {
  font-size: 14px;
}
</style> """


empty_string = """    <tr>
      <th></th>
      <th></th>
      <th></th>
    </tr>"""


def get_image(data, path, requested_from):
	"""
	Функция для сохранения картинки из данного датафрейма
	в заданную директорию

	args:
		data: pandas.DataFrame()
		path: dir
		requested_from: int - Id чата человека, запросившего расписание

	Схема работы:
		1. Формируем все необходимые переменные для создания картинки
		2. Скачиваем файл в папку с расписаниями
		3. Если у нас запрашивали расписание (т.е. requested_from не равен None),
		тогда необходимо отправить его пользователю, иначе - отправить всем погруппно
	"""
	html = css + data.to_html(bold_rows=False).replace(empty_string, '')

	options = {"format": "jpg",
               "encoding": "utf-8",
               "quiet": "",
               "quality": 99,
			   "xvfb": "",
			   "width": 315}
	config = imgkit.config(wkhtmltoimage=path_wkthmltoimage)

	# В зависимости от платформы необходимо правильно преобразовать путь
	# А также по разному использовать imgkit
	try:
		# Если скрипт запущен на windows
		if platform.startswith("win32"):
			path = (path + ".jpg").encode("utf-8")	# Для корректной работы шифруем в UTF-8
			imgkit.from_string(css+html, path, options=options, config=config)
		# Если скрипт запущен на linux
		elif platform.startswith("linux"):
			path = (path + ".jpg").encode("utf-8")
			imgkit.from_string(css+html, path, options=options)
		
		path = path.decode("utf-8")	# А здесь возвращаем из байтового представления в строку

		# Если это расписание появилось на сайте
		if requested_from is None:
			# Добавляем новый файл в бд и отправляем ВСЕМ пользователям по группам
			asyncio.ensure_future(upload_and_send_schedule(path, bot.send_photo, 'photo', None), loop=event_loop)
		
		# Если это расписание у нас запросили
		else:
			# Добавляем новый файл в бд и отправляем пользователю, который запрашивал
			asyncio.ensure_future(upload_and_send_schedule(path, bot.send_photo, 'photo',
														requested_from=requested_from), loop=event_loop)
			

	except Exception as exc:
		print(f"exc: {exc}, path: {path}")
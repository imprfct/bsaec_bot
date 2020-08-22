import imgkit
from .conf import path_wkthmltoimage
from sys import platform

css = """<style type="text/css">
table.dataframe {
  font-family: Tahoma, Geneva, sans-serif;
  border: 0px solid #727272;
  text-align: left;
  border-collapse: collapse;
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


def get_image(data, path):
	"""
	Функция для сохранения картинки из данного датафрейма
	в заданную директорию
	data : pandas.DataFrame()
	path : Windows directory
	"""
	html = css + data.to_html(bold_rows=False).replace(empty_string, '')

	options = {"format": "jpg",
               "encoding": "utf-8",
               "quiet": "",
               "quality": 99,
               "log-level": "none",
               "width": 270}
	config = imgkit.config(wkhtmltoimage=path_wkthmltoimage)

	# В зависимости от платформы необходимо правильно преобразовать путь
	# А также по разному использовать imgkit

	# Если скрипт запущен на windows
	if platform == "win32":
		path = (path + ".jpg").encode("utf-8")
		imgkit.from_string(css+html, path, options=options, config=config)
	# Если скрипт запущен на linux
	elif platform.startswith("linux2"):
		path = (path + ".jpg").encode("utf-8")
		imgkit.from_string(css+html, path, options=options)

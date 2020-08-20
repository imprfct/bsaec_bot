import imgkit
from config import path_wkthmltoimage

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
    
    html = data.to_html(bold_rows=False).replace(empty_string, '')

    text_file = open("process.html", "w", encoding="utf-8")
    text_file.write(css)
    text_file.write(html)
    text_file.close()


    options = {"format": "jpg",
               "encoding": "UTF-8",
               "quiet": "",
               "width": 200}
    config = imgkit.config(wkhtmltoimage=path_wkthmltoimage)

    path = path.replace(" ", "")
    print(path)
    imgkit.from_file("process.html", path+".jpg", options=options, config=config)

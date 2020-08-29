import os
from sys import platform

# === Позже нужно добавить функцию внесения в environ токена бота и моего ид ===
# BOT_TOKEN = os.getenv("BSAEC_BOT_TOKEN")

# admins = [
#     os.getenv("ADMIN_ID"),
# ]

BOT_TOKEN = "1339117782:AAGnpZZZqY8HQ6iY4IZEHevdULzThuWqPY4"

admins = ["504242356"]

spam_account = ["1397240963"]

if platform.startswith("linux"):
    img_path = os.path.join(os.getcwd(), "data/Schedule/")
else:
    img_path = "./data/Schedule"

ip = os.getenv("ip")

aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}

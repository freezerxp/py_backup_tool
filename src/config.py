import json
import os

# Получаю настройки из файла
def get_config():
    curdir = os.getcwd()

    # Открываем JSON-файл для чтения
    with open(curdir + '\\config.json', 'r') as json_file:
        # Загружаем данные из JSON-файла
        return json.load(json_file)

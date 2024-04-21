"""
Скрипт выполняет создание резервных копий для файлов
Создаются архивы, копируются в необходимое расположение
Список файлов и другие настройки в файле backup_config.json
"""

# импортируем модули
import datetime
import os
import config
import messages
import sevenzip
import ya_cloud

# массив сообщений
msgs = []


# добавляем сообщение в массив
def add_msg(msg: str):
    m = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S") + ' | ' + msg + '\n'
    msgs.append(m)
    print(m)


# Создаем бэкап
def do_backup():
    add_msg('Начинаю создание бэкапа файлов')

    cfg = config.get_config()

    for file in cfg['files']:
        # строка даты/времени для имен файлов
        filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        backup_folder_path = (cfg['backupFolder'] + '\\' +
                              cfg['machineName'] + '\\' +
                              'files\\' +
                              file['alias'])

        os.makedirs(backup_folder_path, exist_ok=True)

        data_path = file['path']

        add_msg('Начинаю создание архива для папки: ' + data_path)

        archive_path = backup_folder_path + '\\' + filename + '.zip'

        result = sevenzip.create_archive(data_path, archive_path)

        add_msg(result['message'])

        if cfg['yandexCloud']['enable']:
            cloud_result = ya_cloud.upload_file(archive_path)
            add_msg(cloud_result['message'])


    add_msg('Резервное копирование заверешно')

    messages.sendMsg(''.join(msgs))

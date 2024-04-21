# импортируем модули
import datetime
import os
import subprocess
import messages
import sevenzip
import config
import ya_cloud

msgs = []


def add_msg(msg: str):
    m = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S") + ' | ' + msg + '\n'
    msgs.append(m)
    print(m)


def do_backup():

    add_msg('Начинаю создание бэкапа баз данных')

    cfg = config.get_config()

    # утилита для дампов
    mysqldump = cfg['paths']['mysqldump']

    mysql_array = cfg['mysql']

    for mysql in mysql_array:

        # базы данных
        dbarray = mysql['dbs']

        # аргументы для авторизации
        dbuser = mysql['auth']['user']
        dbpass = mysql['auth']['pass']

        # для всех БД в массиве
        for db in dbarray:
            add_msg('Начинаю создание архива для БД: ' + db)
            # подпапка для бэкапа
            backup_folder_path = (cfg['backupFolder'] + '\\' +
                                  cfg['machineName'] + '\\' +
                                  'mysql\\' +
                                  mysql['alias'])

            # создаю подпапку
            os.makedirs(backup_folder_path, exist_ok=True)

            # имена для файлов
            filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

            # имя файла дампа
            dump_file_name = backup_folder_path + '\\' + filename + '(' + db + ').sql'

            # запускаю создание дампа
            output = subprocess.run([mysqldump,
                                     '--user=' + dbuser,
                                     '--password=' + dbpass,
                                     '--result-file=' + dump_file_name,
                                     '--databases', db],
                                    shell=True,
                                    capture_output=True)
            print(output.stdout)

            # имя файла архива
            archive_path = backup_folder_path + '\\' + filename + '.zip'

            result = sevenzip.create_archive(dump_file_name, archive_path)
            add_msg(result['message'])

            if cfg['yandexCloud']['enable']:
                cloud_result = ya_cloud.upload_file(archive_path)
                add_msg(cloud_result['message'])

            # удаляю файл дампа
            os.remove(dump_file_name)

    add_msg('Завершено')
    messages.sendMsg(''.join(msgs))

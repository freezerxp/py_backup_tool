import config
import subprocess
import os
import humanize
import ya_cloud


#Создание архива
def create_archive(data_path, archive_path):
    try:
        #Получаем настройки
        cfg = config.get_config()

        #Путь к исполняющему файлу 7zip.exe
        seven_zip = cfg['paths']['sevenzip']

        #Запуск команды
        output = subprocess.run([seven_zip, 'a', archive_path, data_path],
                                shell=True,
                                capture_output=True)
        print(output.stdout)

        #Получаем размер архива
        archive_size = os.path.getsize(archive_path)

        human_size = humanize.naturalsize(archive_size)

        return {"result": True,
                "message": 'Создан архив: ' + archive_path + ', ' + human_size}
    except Exception as e:
        return {"result": False,
                'message': 'При создании архива возникло исклчючение: ' + e}

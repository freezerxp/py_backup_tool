#импортируем модули
import datetime
import os
import subprocess
import json
import mesages
import humanize #требуется установка модуля

msgs = []

def addMsg(msg):
    m= datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S") + ' | ' + msg + '\n'
    msgs.append(m)
    print(m)

def doBackup():
    #объявлем переменные
    addMsg('Начинаю создание бэкапа баз данных')

    curdir = os.getcwd()
    # Открываем JSON-файл для чтения
    with open(curdir+'\\backup_config.json', 'r') as json_file:
        # Загружаем данные из JSON-файла
        data = json.load(json_file)

    #утилита для дампов
    mysqldump = data['paths']['mysqldump']

    #путь к 7zip архиватору
    sevenzip = data['paths']['sevenzip']

    #папка для бэкапов
    backupfolder = data['mysql']['backupFolder']

    #базы данных
    dbarray = data['mysql']['dbs']

    #аргументы для авторизации
    dbuser = data['mysql']['auth']['user']
    dbpass = data['mysql']['auth']['pass']

    ############################



    #для всех БД в массиве
    for db in dbarray:
       
        addMsg('Начинаю создание архива для БД: '+db)
        #подпапка для бэкапа
        sub_backupfolder = backupfolder + '\\' + db

        #создаю подпапку
        os.makedirs(sub_backupfolder, exist_ok=True)

        #имена для файлов
        filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        #имя файла дампа
        dumpFileName = sub_backupfolder +'\\' + filename +'('+db+').sql'

        #запускаю создание дампа
        output = subprocess.run([mysqldump, '--user='+dbuser, '--password='+dbpass, '--result-file='+dumpFileName, '--databases', db], shell=True, capture_output=True)
        print(output.stdout)

        #имя файла архива
        archiveFileName = sub_backupfolder +'\\' + filename + '.zip'

        #создаю архив
        output = subprocess.run([sevenzip, 'a', archiveFileName, dumpFileName], shell=True, capture_output=True)
        print(output.stdout)
        aSize = os.path.getsize(archiveFileName)
        #удаляю файл дампа
        os.remove(dumpFileName)
        addMsg('Создан архив: '+archiveFileName + ', ' + humanize.naturalsize(aSize))

    addMsg('Завершено')
    mesages.sendMsg(''.join(msgs))

"""
Скрипт для создания резервных копий git-репозиториев с github
"""

#импортируем модули
import subprocess
import os
import json
import datetime
import messages
import humanize #требуется установка модуля
import send2trash #требуется установка модуля. Используется для удаления файлов, т.к. shutil.rmtree не может удалить...

#массив сообщений
msgs = []

#добавляем сообщение в массив
def addMsg(msg):
    m= datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S") + ' | ' + msg + '\n'
    msgs.append(m)
    print(m)



def doBackup():
    addMsg('Начинаю создание бэкапа репозиториев')

    curdir = os.getcwd()

    # Открываем настройки резеврного копирования
    with open(curdir+'\\config.json', 'r') as json_file:
        # Загружаем данные из JSON-файла
        backupConfig = json.load(json_file)

    sevenzip=backupConfig['paths']['sevenzip']

    # Ваш Personal Access Token
    access_token = backupConfig['git']['token']

    owner = backupConfig['git']['owner']

    # Путь к временной папке для клонирования
    temp_folder =  'c:\\git_backup\\temp\\'

    if os.path.exists(temp_folder):
        send2trash.send2trash(temp_folder)

    gitExe = backupConfig['paths']['gitExe']

    for r in backupConfig['git']['repositories']:
        addMsg('Клонирую репозиторий: ' +r)
        # URL репозитория на GitHub
        repo_url = f'https://{owner}:{access_token}@github.com/{owner}/{r}.git'

        repo_folder = f'{temp_folder}\\{r}\\'
        os.makedirs(repo_folder, exist_ok=True)

        # Формируем команду для клонирования репозитория с использованием токена
        command = f'"{gitExe}" clone {repo_url} {repo_folder}'
       
        process = subprocess.Popen(command, shell=True,  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        # Выводим результат выполнения команды
        if process.returncode == 0:
            addMsg('Репозиторий успешно клонирован.')
        else:
            addMsg(f'Ошибка при клонировании репозитория:\n{stderr.decode()}')

        filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        #Упаковываю в архив
        archivePath = backupConfig['git']['backupFolder'] + '\\' + r + '\\' + filename + '.zip'
        output = subprocess.run([sevenzip, 'a', archivePath, repo_folder], shell=True, capture_output=True)
        print(output.stdout)
        aSize = os.path.getsize(archivePath)
        addMsg('Создан архив: ' + archivePath + ', ' + humanize.naturalsize(aSize))

    send2trash.send2trash(temp_folder)

    addMsg('Создание бэкапа репозиториев заверешно')
    messages.sendMsg(''.join(msgs))

"""
Скрипт для создания резервных копий git-репозиториев с github
"""

# импортируем модули
import subprocess
import os
import config
import datetime
import sevenzip
import messages

# требуется установка модуля. Используется для удаления файлов,
# т.к. shutil.rmtree не может удалить...
import send2trash

# массив сообщений
msgs = []


# добавляем сообщение в массив
def add_msg(msg: str):
    m = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S") + ' | ' + msg + '\n'
    msgs.append(m)
    print(m)


def do_backup():
    add_msg('Начинаю создание бэкапа репозиториев')

    cfg = config.get_config()

    # Ваш Personal Access Token
    access_token = cfg['git']['token']

    user = cfg['git']['user']

    # Путь к временной папке для клонирования
    temp_folder = 'c:\\git_backup\\temp\\'

    if os.path.exists(temp_folder):
        send2trash.send2trash(temp_folder)

    git_exe = cfg['paths']['gitExe']

    for repo in cfg['git']['repositories']:
        repo_owner = repo['owner']
        repo_name = repo['name']

        add_msg(f'Клонирую репозиторий: {repo_owner}/{repo_name}')

        # URL репозитория на GitHub
        repo_url = f'https://{user}:{access_token}@github.com/{repo_owner}/{repo_name}.git'

        repo_folder = f'{temp_folder}\\{repo_owner}\\{repo_name}\\'
        os.makedirs(repo_folder, exist_ok=True)

        # Формируем команду для клонирования репозитория с использованием токена
        command = f'"{git_exe}" clone {repo_url} {repo_folder}'

        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        # Выводим результат выполнения команды
        if process.returncode == 0:
            add_msg('Репозиторий успешно клонирован.')
        else:
            add_msg(f'Ошибка при клонировании репозитория:\n{stderr.decode()}')

        filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # Упаковываю в архив
        backup_folder_path = (cfg['backupFolder'] + '\\' +
                              cfg['machineName'] + '\\' +
                              'git\\' +
                              repo_owner + '\\' +
                              repo_name)

        archive_path = backup_folder_path + '\\' + filename + '.zip'
        result = sevenzip.create_archive(repo_folder, archive_path)
        add_msg(result['message'])

    send2trash.send2trash(temp_folder)

    add_msg('Создание бэкапа репозиториев заверешно')
    messages.sendMsg(''.join(msgs))

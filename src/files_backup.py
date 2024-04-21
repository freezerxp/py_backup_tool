"""
Скрипт выполняет создание резервных копий для файлов
Создаются архивы, копируются в необходимое расположение
Список файлов и другие настройки в файле backup_config.json
"""


#импортируем модули
import datetime
import os
import subprocess
import json
import messages 

#массив сообщений
msgs = []

#добавляем сообщение в массив
def addMsg(msg):
	m= datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S") + ' | ' + msg + '\n'
	msgs.append(m)
	print(m)
	
#Создаем бэкап
def doBackup():

	addMsg('Начинаю создание бэкапа файлов')

	curdir = os.getcwd()

	# Открываем JSON-файл для чтения
	with open(curdir+'\\config.json', 'r') as json_file:
	    # Загружаем данные из JSON-файла
	    data = json.load(json_file)

	#путь к 7zip архиватору
	sevenzip = data['paths']['sevenzip']

	for f in data['files']:
		#строка даты/времени для имен файлов
		filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

		os.makedirs(f['backup'], exist_ok=True)

		addMsg('Начинаю создание архива для папки: ' + f['data'])

		archivePath=f['backup'] + '\\' + filename + '.zip'
		output = subprocess.run([sevenzip, 'a', archivePath, f['data']], shell=True, capture_output=True)
		print(output.stdout)
		aSize = os.path.getsize(archivePath)
		addMsg('Создан архив: ' + archivePath + ', ' + humanize.naturalsize(aSize))

	addMsg('Резервное копирование заверешно')


	messages.sendMsg(''.join(msgs))
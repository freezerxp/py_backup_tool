from rocketchat_API.rocketchat import RocketChat
import os
import json

curdir = os.getcwd()

# Открываем JSON-файл для чтения
with open(curdir+'\\config.json', 'r') as json_file:
    # Загружаем данные из JSON-файла
    data = json.load(json_file)['rocketChat']

def sendMsg(message):
	if(data['enable'] == True):
		sendMsgToRocketChat(message)



def sendMsgToRocketChat(message):
    # Указать URL вашего Rocket.Chat сервера
	rocket_chat_url = data['server']
	# Указать логин и пароль для доступа к API вашего Rocket.Chat сервера
	username = data['user']
	password = data['pass']

	# Создание экземпляра RocketChat API
	rocket = RocketChat(username, password, server_url=rocket_chat_url)

	# Отправка сообщения в канал
	channel_name = data['channel']
	rocket.chat_post_message(message, channel=channel_name)

def sendMsgToTelegram(message):
	return
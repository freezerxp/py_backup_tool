from rocketchat_API.rocketchat import RocketChat #необходима установка модуля rocketchat_API
from telegram import Bot #неоходима установка модуля python-telegram-bot

import os
import json

curdir = os.getcwd()

# Открываем JSON-файл для чтения
with open(curdir+'\\config.json', 'r') as json_file:
    # Загружаем данные из JSON-файла
    data = json.load(json_file)

def sendMsg(message):
	if(data['rocketChat']['enable'] == True):
		sendMsgToRocketChat(message)
	if(data['telegram']['enable'] == True):
		sendMsgToTelegram(message)

def sendMsgToTg(message):
	chat_id= data['telegram']['chatId']
    bot = Bot(token=data['telegram']['toketn'])
    bot.send_message(chat_id=chat_id, text=message)


def sendMsgToRocketChat(message):
    # Указать URL вашего Rocket.Chat сервера
	rocket_chat_url = data['rocketChat']['server']
	# Указать логин и пароль для доступа к API вашего Rocket.Chat сервера
	username = data['rocketChat']['user']
	password = data['rocketChat']['pass']

	# Создание экземпляра RocketChat API
	rocket = RocketChat(username, password, server_url=rocket_chat_url)

	# Отправка сообщения в канал
	channel_name = data['rocketChat']['channel']
	rocket.chat_post_message(message, channel=channel_name)

def sendMsgToTelegram(message):
	return
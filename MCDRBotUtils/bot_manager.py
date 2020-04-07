# -*- coding: utf-8 -*-
from .pycraft.networking import connection
import traceback

FILE_PATH = './plugins/MCDRBotUtils/port.ini'
port = None


def load_port():
	global port
	try:
		with open(FILE_PATH) as handle:
			port = int(handle.read())
	except:
		print('[MCD-bot]: failed to read port from config file, using default')
		print(traceback.format_exc())
		port = 25565
		with open(FILE_PATH, 'w') as handle:
			handle.write(str(port))
	return port


class Bot:
	def __init__(self, name):
		global port
		self.name = name
		self.bot = connection.Connection('127.0.0.1', port, None, name)
		self.bot.connect()

	def stop(self):
		self.bot.disconnect()

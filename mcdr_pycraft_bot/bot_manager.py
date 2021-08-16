from threading import RLock
from typing import List, Dict, Optional

from mcdreforged.api.all import *

from .minecraft.networking import connection


class Bot:
	def __init__(self, bot_list: 'BotStorage', name: str, port: int):
		self.name = name
		self.bot = connection.Connection(
			address='127.0.0.1',
			port=port,
			auth_token=None,
			username=name,
			handle_exit=lambda: bot_list.on_disconnected(self)
		)
		self.bot.connect()
		print(self.bot.networking_thread)
		self.bot.networking_thread.setName('MCDR Bot {}'.format(self.name))

	def stop(self):
		self.bot.disconnect()


class BotStorage(Dict[str, Bot]):
	def __init__(self):
		super().__init__()
		self.__lock = RLock()

	def add_bot(self, name: str, port: int):
		bot = Bot(self, name, port)
		with self.__lock:
			self[name] = bot

	def get_bot(self, name: str) -> Optional[Bot]:
		with self.__lock:
			return self.get(name)

	def is_bot(self, name: str) -> bool:
		return self.get_bot(name) is not None

	def remove_bot(self, name: str) -> bool:
		bot = self.get_bot(name)
		if bot is not None:
			bot.stop()
			return True
		else:
			return False

	def on_disconnected(self, bot: Bot):
		with self.__lock:
			self.pop(bot.name, None)
		ServerInterface.get_instance().logger.info('MCDR Bot {} disconnected'.format(bot.name))

	def get_bot_name_list(self) -> List[str]:
		with self.__lock:
			return list(self.keys())

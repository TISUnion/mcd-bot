from threading import RLock
from typing import List, Dict, Optional

from mcdreforged.api.all import *

from .minecraft.networking import connection


class Bot:
	def __init__(self, name: str, address: str, port: int):
		self.name = name
		self.connection = connection.Connection(
			address=address,
			port=port,
			auth_token=None,
			username=name,
			handle_exception=self.handle_exception
		)
		self.connection.connect()

	def stop(self):
		self.connection.disconnect()

	def handle_exception(self, exc, exc_info):
		ServerInterface.get_instance().logger.warning('Exception at MCDR bot {}: {}'.format(self.name, exc))


class BotStorage(Dict[str, Bot]):
	def __init__(self):
		super().__init__()
		self.__lock = RLock()
		self.__patch_pycraft()

	@staticmethod
	def __patch_pycraft():
		from mcdr_pycraft_bot.minecraft.networking.connection import NetworkingThread
		NetworkingThread.getName = lambda self: 'MCDR Bot {}'.format(self.connection.username)

	def add_bot(self, name: str, address: str, port: int) -> bool:
		bot = Bot(name, address, port)
		if bot.connection.connected:
			with self.__lock:
				self[name] = bot
		return bot.connection.connected

	def get_bot(self, name: str) -> Optional[Bot]:
		with self.__lock:
			return self.get(name)

	def is_bot(self, name: str) -> bool:
		return self.get_bot(name) is not None

	def remove_bot(self, name: str) -> bool:
		with self.__lock:
			bot = self.pop(name, None)
		if bot is not None:
			try:
				bot.stop()
			except:
				pass
			return True
		else:
			return False

	def get_bot_name_list(self) -> List[str]:
		with self.__lock:
			return list(self.keys())

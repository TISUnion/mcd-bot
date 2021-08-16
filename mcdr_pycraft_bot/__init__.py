import re
from typing import Optional

from mcdreforged.api.all import *
from mcdr_pycraft_bot.bot_manager import BotStorage


class Config(Serializable):
	port: int = 25565
	gamemode: str = 'survival'


config: Config

HELP_MESSAGE = '''
------ MCDR BOT ------
命令帮助如下:
§7!!bot add §b<name>§r：召唤一个bot，名称为§bbot_<name>§r
§7!!bot stop §b<name>§r：让名称为§b<name>§r的bot离开游戏
§7!!bot tp §b<name>§r：让名称为§b<name>§r的bot传送到你的位置
§7!!bot clean§r：使所有bot离开游戏
'''.strip()

bot_storage = BotStorage()


def reply(source: CommandSource, msg):
	source.reply('[MCDR-bot] ' + msg)


def add_bot(source: CommandSource, name: str):
	if not name.startswith('bot_'):
		name = 'bot_' + name
	if not re.fullmatch(r'\w{1,16}', name):
		reply(source, 'Bot名字不合法！')
	if bot_storage.is_bot(name):
		reply(source, 'Bot {}已经存在!'.format(name))
	else:
		@new_thread('bot connection')
		def connect():
			bot_storage.add_bot(name, config.port)
		connect()


def remove_bot(source: CommandSource, name: str):
	if bot_storage.remove_bot(name):
		reply(source, '已清除Bot {}'.format(name))
	else:
		reply(source, 'Bot {}不存在!'.format(name))


def tp_bot(source: PlayerCommandSource, name: str):
	bot = bot_storage.get_bot(name)
	if bot is None:
		reply(source, 'Bot {}不存在!'.format(name))
	else:
		reply(source, '传送中...')
		source.get_server().execute('execute at {0} run tp {1} {0}'.format(source.player, name))


def remove_all(source: Optional[CommandSource]):
	for bot_name in bot_storage.get_bot_name_list():
		bot_storage.remove_bot(bot_name)
	if source is not None:
		reply(source, 'bot已清空')


def on_player_joined(server, player, info):
	if bot_storage.is_bot(player):
		server.execute('gamemode {} {}'.format(config.gamemode, player))


def on_load(server: PluginServerInterface, old):
	global bot_storage, config
	if old is not None:
		bot_storage = old.bot_storage
	config = server.load_config_simple(target_class=Config)
	server.register_help_message('!!bot', 'MCDR Bot相关指令')

	def bot_name():
		return Text('bot_name').suggests(lambda: bot_storage.get_bot_name_list())

	server.register_command(
		Literal('!!bot').
		runs(lambda src: src.reply(HELP_MESSAGE)).
		then(Literal('add').then(bot_name().runs(lambda src, ctx: add_bot(src, ctx['bot_name'])))).
		then(Literal('stop').then(bot_name().runs(lambda src, ctx: remove_bot(src, ctx['bot_name'])))).
		then(
			Literal('tp').
			requires(lambda src: src.is_player, lambda: '需要玩家执行此命令').
			then(bot_name().runs(lambda src, ctx: tp_bot(src, ctx['bot_name'])))
		).
		then(Literal('clean').runs(remove_all))
	)


def on_server_stop(server, code):
	remove_all(None)

import re
from typing import Optional, Any, Callable

from mcdreforged.api.all import *
from mcdr_pycraft_bot.bot_manager import BotStorage


class Config(Serializable):
	address: str = '127.0.0.1'
	port: int = 25565
	gamemode: str = 'survival'
	name_prefix: str = 'bot_'


config: Config

HELP_MESSAGE = '''
------ MCDR BOT ------
命令帮助如下:
§7!!bot add §b<name>§r：召唤一个bot，名称为§bbot_<name>§r
§7!!bot stop §b<name>§r：让名称为§b<name>§r的bot离开游戏
§7!!bot tp §b<name>§r：让名称为§b<name>§r的bot传送到你的位置
§7!!bot list§r：列出当前所有的bot名称
§7!!bot clean§r：使所有bot离开游戏
见配置文件以了解更多设置
'''.strip()

bot_storage = BotStorage()


def reply(source: CommandSource, msg):
	source.reply('[MCDR-Bot] ' + msg)


def add_bot(source: CommandSource, name: str):
	if not name.startswith(config.name_prefix):
		name = config.name_prefix + name
	if not re.fullmatch(r'\w{1,16}', name):
		reply(source, 'bot名字{}不合法！'.format(name))
	if bot_storage.is_bot(name):
		reply(source, 'bot {}已经存在!'.format(name))
	else:
		@new_thread('bot connection')
		def connect():
			succeed = bot_storage.add_bot(name, config.address, config.port)
			if not succeed:
				reply(source, 'bot {}连接服务器失败')
		connect()


def remove_bot(source: CommandSource, name: str):
	if bot_storage.remove_bot(name):
		reply(source, '已清除bot {}'.format(name))
	else:
		reply(source, 'bot {}不存在!'.format(name))


def tp_bot(source: PlayerCommandSource, name: str):
	bot = bot_storage.get_bot(name)
	if bot is None:
		reply(source, 'bot {}不存在!'.format(name))
	else:
		reply(source, '传送中...')
		source.get_server().execute('execute at {0} run tp {1} {0}'.format(source.player, name))


def remove_all(source: Optional[CommandSource]):
	for bot_name in bot_storage.get_bot_name_list():
		bot_storage.remove_bot(bot_name)
	if source is not None:
		reply(source, 'bot已清空')


def list_bots(source: CommandSource, reply_func: Callable[[CommandSource, Any], Any] = reply):
	name_list = bot_storage.get_bot_name_list()
	reply_func(source, 'bot列表：{}'.format('' if len(name_list) > 0 else '空'))
	for bot_name in name_list:
		reply_func(source, RText.format(
			'- {} {}',
			RText('[x]', RColor.red).h('{}给我下线'.format(bot_name)).c(RAction.suggest_command, '!!bot stop {}'.format(bot_name)),
			bot_name
		))


def send_help(source: CommandSource):
	source.reply(HELP_MESSAGE)
	list_bots(source, type(source).reply)


def on_player_joined(server, player: str, info):
	if bot_storage.is_bot(player):
		server.execute('gamemode {} {}'.format(config.gamemode, player))


def on_player_left(server, player: str):
	if bot_storage.is_bot(player):
		bot_storage.remove_bot(player)


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
		runs(send_help).
		then(Literal('add').then(bot_name().runs(lambda src, ctx: add_bot(src, ctx['bot_name'])))).
		then(Literal('stop').then(bot_name().runs(lambda src, ctx: remove_bot(src, ctx['bot_name'])))).
		then(
			Literal('tp').
			requires(lambda src: src.is_player, lambda: '需要玩家执行此命令').
			then(bot_name().runs(lambda src, ctx: tp_bot(src, ctx['bot_name'])))
		).
		then(Literal('list').runs(lambda src: list_bots(src))).
		then(Literal('clean').runs(remove_all))
	)


def on_server_stop(server, code):
	remove_all(None)

# -*- coding: utf-8 -*-
import re
import sys

sys.path.append("plugins/")
import MCDRBotUtils.bot_manager as bot_manager


HELP_MESSAGE = '''
------ MCDR BOT ------
命令帮助如下:
§7!!bot add §b<name>§r：召唤一个bot，名称为§bbot_<name>§r
§7!!bot stop §b<name>§r：让名称为§b<name>§r的bot离开游戏
§7!!bot tp §b<name>§r：让名称为§b<name>§r的bot传送到你的位置
§7!!bot clean§r：使所有bot离开游戏
'''.strip()
GAMEMODE = 'survival'

bot_list = []


def reply(server, info, msg):
	server.reply(info, '[MCDR-bot] ' + msg)


def add_bot(bot_name):
	global bot_list
	bot = bot_manager.Bot(bot_name)
	bot_list.append(bot)


def get_bot(bot_name):
	for bot in bot_list:
		if bot.name == bot_name:
			return bot
	return None


def remove_bot(bot_name):
	global bot_list
	bot = get_bot(bot_name)
	bot.stop()
	bot_list.remove(bot)


def remove_all():
	global bot_list
	for bot in bot_list:
		bot.stop()
	bot_list = []


def on_info(server, info):
	if info.is_user:
		if info.content.startswith('!!bot'):
			args = info.content.split(' ')
			global bot_list
			if args[0] == '!!bot':
				if len(args) == 1:
					server.reply(info, HELP_MESSAGE)
				elif args[1] == 'add' and len(args) == 3:
					bot_name = 'bot_' + args[2]
					if not re.fullmatch(r'\w{1,16}', bot_name):
						reply(server, info, 'Bot名字不合法！')
					if get_bot(bot_name):
						reply(server, info, 'Bot已经存在!')
					else:
						add_bot(bot_name)
				elif args[1] == 'stop' and len(args) == 3:
					remove_bot(args[2])
				elif args[1] == 'tp' and len(args) == 3 and info.is_player:
					bot_name = args[2]
					if get_bot(bot_name):
						reply(server, info, '传送中...')
						server.execute('execute at {0} run tp {1} {0}'.format(info.player, bot_name))
				elif args[1] == 'clean' and len(args) == 2:
					remove_all()
					reply(server, info, 'bot已清空')
				else:
					reply(server, info, '参数格式不正确')


def on_player_joined(server, player):
	if get_bot(player):
		server.execute('gamemode {} {}'.format(GAMEMODE, player))


def on_load(server, old):
	bot_manager.load_port()
	if old is not None:
		global bot_list
		bot_list = old.bot_list
	server.add_help_message('!!bot', 'Bot相关指令')


def on_server_stop(server, code):
	remove_all()

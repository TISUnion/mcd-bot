# -*- coding: utf-8 -*-
import copy
import os
import sys
from time import sleep
import json

helpmsg = '''=====MCD BOT=====
命令帮助如下:
!!bot add (注释) [-keep] [-f(force)]：召唤一个bot,使用-keep参数使bot在你下线后不下线,使用-f强制忽略bot前缀
!!bot stop (name)：让bot离开游戏
!!bot tp (name)：让bot传送到你的地方
!!bot gm (name) (c/s)：设置bot的gamemode(Creative / Spectator)
!!bot kickall：!慎用!使所有bot退出游戏，请在重载插件之前使用
'''

botlist = []
namelist = []
config = {}
default = 'protocol'

try:
  with open('./config/mcdbot.json','r') as handle:
    config = json.load(handle)
except:
  print('could not open config file, using default(' + default + ')')
  config['mode'] = default
  if not os.path.isdir('./config'):
    os.makedirs('./config')
  with open('./config/mcdbot.json','w') as handle:
    json.dump(config, handle)

sys.path.append("plugins/")
if config['mode'] == 'carpet':
  from mcdbotUtils.carpetbot import mcbot
  mode = 'carpet'
else:
  from mcdbotUtils.botmanager import mcbot
  mode = 'network'

def onServerInfo(server, info):
  if (info.isPlayer == 1):
    if info.content.startswith('!!bot'):
      args = info.content.split(' ')
      global namelist
      global botlist
      if args[0] == '!!bot':
        if len(args) == 1:
          for line in helpmsg.splitlines():
            server.tell(info.player, line)
        elif (args[1] == 'mode'):
          server.say(config['mode'])
        elif (args[1] == 'add') and (len(args)>2):
          if ' -f' in info.content:
            args = info.content.replace(' -f', '').split(' ')
            botname = 'bot_' + args[2]
          else:
            botname = info.player + '_b_'+ args[2]
          if (len(botname)>16):
            server.tell(info.player, '[MCD-bot]:名字太长（请控制在16个字符以内）')
          if botname in namelist:
            server.tell(info.player, 'bot已经存在!')
          else:
            if (len(args) == 4) and (args[3] == '-keep'):
              if config['mode'] == 'carpet':
                bot = mcbot(botname, info.player, server, 1)
              else:
                bot = mcbot(botname, info.player, 1)
            else:
              if config['mode'] == 'carpet':
                bot = mcbot(botname ,info.player, server)
              else:
                bot = mcbot(botname, info.player)
            sleep(0.1)
            server.execute('gamemode creative ' + botname)
            botlist.append(bot)
            namelist.append(botname)
        elif (args[1] == 'stop') and (len(args) == 3):
          botname = args[2]
          if botname in namelist:
            namelist.remove(botname)
            for bot in botlist:
              if bot.name == botname:
                if config['mode'] == 'carpet':
                  bot.stop(server)
                else:
                  bot.stop()
                botlist.remove(bot)
        elif (args[1] == 'tp') and (len(args) == 3):
          if args[2] in namelist:
            for bot in botlist:
              if bot.name == args[2]:
                if bot.owner == info.player:
                  server.tell(info.player, 'Teleporting...')
                  server.execute('execute at ' + info.player + ' run tp ' + args[2] + ' ' + info.player)
                else:
                  server.tell(info.player, '你不是这个bot的主人')
        elif (args[1] == 'gm') and (len(args) == 4):
          if args[2] in namelist:
            for bot in botlist:
              if bot.name == args[2]:
                if bot.owner == info.player:
                  if args[3] == 'c':
                    server.execute('gamemode creative ' + args[2])
                  if args[3] == 's':
                    server.execute('gamemode spectator ' + args[2])
                else:
                  server.tell(info.player, '你不是这个bot的主人')
        elif (args[1] == 'kickall') and (len(args) == 2):
          namelist = []
          for bot in botlist:
            bot.stop()
          botlist = []
          server.say('bot已清空')
        else:
          server.tell(info.player, '参数格式不正确')


def onPlayerLeave(server, player):
  global namelist
  global botlist
  removelist = []
  for bot in botlist:
    if (bot.owner == player) and (bot.keep == 0):
      namelist.remove(bot.name)
      if config['mode'] == 'carpet':
        bot.stop(server)
      else:
        bot.stop()
      removelist.append(bot)
  for bot in removelist:
    botlist.remove(bot)


def on_info(server, info):
  info2 = copy.deepcopy(info)
  info2.isPlayer = info2.is_player
  onServerInfo(server, info2)


def on_player_left(server, player):
  onPlayerLeave(server, player)


def on_load(server, old):
  if old is not None:
    global namelist, botlist
    namelist = old.namelist
    botlist = old.botlist

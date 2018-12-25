# -*- coding: utf-8 -*-

from plugins.mcdbotUtils.botmanager import mcbot

botlist = []

def onServerInfo(server, info):
  if (info.isPlayer == 1):
    if info.content.startswith('!!bot'):
      args = info.content.split(' ')
      if args[0] == '!!bot':
        if len(args) == 2:
          bot = mcbot(args[1])
          botlist.append(bot)

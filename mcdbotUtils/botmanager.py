# -*- coding: utf-8 -*-

from minecraft.networking import connection as conn
import traceback

try:
  with open('./plugins/mcdbotUtils/port.ini','r') as handle:
    port = int(handle.read())
except:
  print('[MCD-bot]: failed to read port from config file,using default')
  print(traceback.format_exc())
  port = 25565

class mcbot(object):
  def __init__(self, name, owner, bot_id):
    self.start(name, owner, bot_id)
  
  def start(self, name, owner, bot_id):
    self.bot = conn.Connection('127.0.0.1', port, None, name)
    self.bot.connect()
    self.owner = owner
    self.bot_id = bot_id

  def stop(self):
    try:
      self.bot.disconnect()
    except EOFError:
      pass
      
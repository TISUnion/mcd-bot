# -*- coding: utf-8 -*-

from .minecraft.networking import connection as conn
import traceback

try:
  with open('./plugins/mcdbotUtils/port.ini','r') as handle:
    port = int(handle.read())
except:
  print('[MCD-bot]: failed to read port from config file,using default')
  print(traceback.format_exc())
  port = 25565

class mcbot(object):
  def __init__(self, name, owner, keep=0):
    self.start(name, owner, keep)
  
  def start(self, name, owner, keep):
    self.bot = conn.Connection('127.0.0.1', port, None, name)
    self.bot.connect()
    self.owner = owner
    self.name = name
    self.keep = keep

  def stop(self):
    self.bot.disconnect()
      
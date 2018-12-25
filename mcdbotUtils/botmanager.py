# -*- coding: utf-8 -*-

from minecraft.networking import connection as conn

with open('./plugins/mcdbotUtils/port.ini','r') as handle:
  port = int(handle.read())

class mcbot(object):
  def __init__(self, name):
    self.start(name)
  
  def start(self, name):
    self.bot = conn.Connection('127.0.0.1', port, None, name)
    self.bot.connect()

  def stop(self):
    self.bot.disconnect()

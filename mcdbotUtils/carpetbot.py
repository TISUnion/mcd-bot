# -*- coding: utf-8 -*-

import traceback

try:
  with open('./plugins/mcdbotUtils/port.ini','r') as handle:
    port = int(handle.read())
except:
  print('[MCD-bot]: failed to read port from config file,using default')
  print(traceback.format_exc())
  port = 25565

class mcbot(object):
  def __init__(self, name, owner, server, keep=0):
    self.start(name, owner, keep, server)
  
  
  def start(self, name, owner, keep, server):
    server.execute('player ' + name + ' spawn')
    self.owner = owner
    self.name = name
    self.keep = keep

  def stop(self, server):
    server.execute('player ' + self.name + ' kill')
from PluginBot import PRIVMSG
from time import sleep
from random import randint
from threading import Thread
import codecs

codecs.register(lambda name: codecs.lookup("utf-8") if name == "cp65001" else None)

class Flag:
	flag = False
myFlag = Flag()

class CheckFlag(Thread):
	parent = None
	channel = None

	def __init__(self, parent, channel):
		super().__init__()
		self.parent = parent
		self.channel = channel

	def run(self):
		print("Waiting.")
		sleep(4 + (randint(1, 15) / 3))
		print("Any actions afterwards? ", myFlag.flag)
		if (myFlag.flag == False):
			print("sending.")
			self.parent.s.send(PRIVMSG(self.channel, "@bef", 0))



def version():
	myFlag.flag = False
	return "This is a temp cheat bot. - 0.1"

def plugin_main(parent, tokens):
	if (any("@bef" in a for a in tokens) or any("@bang" in a for a in tokens)):
		print("Duck Taken.")
		myFlag.flag = True
	elif ((any("\\_" in a for a in tokens) or any("\\?_" in a for a in tokens)) and not myFlag.flag and (tokens[0] == "Saltbot")):
		print("Detected Saltbot")
		checkFlag = CheckFlag(parent, tokens[2])
		myFlag.flag = False
		checkFlag.start()
		
import os
import atexit
import string
import importlib
import threading
from time import sleep

def BYTE(message):
	return bytes("%s\r\n" % message, "UTF-8")

class UserInput(threading.Thread):
	isRunning = False
	parent = None

	def __init__(self, bot):
		super().__init__()
		self.parent = bot
		self.isRunning = False
		self.start()

	def createMessage(self, message):
		temp = ""
		for i in range(len(message)):
			if (i != len(message) - 1):
				temp += message[i] + " "
			else:
				temp += message[i]
		return temp

	def run(self):
		self.isRunning = True
		while (self.isRunning):
			try:
				message = input()
				message = message.split(" ")
				if (message[0] != ""):
					if (message[0] == "/reload"):
						print("Reloading all plugins.")
						self.parent.reloadAll()
					elif (message[0] == "/quit"):
						print("Quitting.")
						self.parent.quit()
						self.parent.isRunning = False
						self.isRunning = False
					elif (message[0] == "/j"):
						if (len(message) < 2 or len(message) > 2):
							print("Incorrect usage.")
						else:
							self.parent.switch(message[1])
					else:
						self.parent.s.send(BYTE("PRIVMSG %s :%s" % (self.parent.channel, self.createMessage(message))))
			except Exception as error:
				print(error)
		

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
		self.setDaemon(True)
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
						self.parent.reloadAll()
					elif (message[0] == "/quit"):
						print("Quitting.")
						self.parent.quit()
						self.isRunning = False
					elif (message[0] == "/j"):
						if (len(message) < 2 or len(message) > 2):
							print("Incorrect usage.")
						else:
							self.parent.switch(message[1])
					elif (message[0] == "/help"):
						print("1. Type anything to chat with others in %s." % self.parent.focusedChannel)
						print("2. /help -- Bring up the bot commands.")
						print("3. /j -- Join a new channel. Channel focus will switch over.")
						print("4. /reload -- Reload all plugins. (Hotswapping is supported.)")
						print("5. /quit -- Quit the bot.")
					else:
						self.parent.s.send(BYTE("PRIVMSG %s :%s" % (self.parent.focusedChannel, self.createMessage(message))))
			except Exception as error:
				print(error)
		

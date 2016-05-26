import os
import sys
import random
import socket
import string
import importlib
import atexit
import threading
import traceback
from time import sleep

import UserInput


#For distribution, it will connect to #wedrbot.

def BYTE(message):
	return bytes("%s\r\n" % message, "UTF-8")

def PRIVMSG(recipient, message, mode):
	if (mode == 0):
		return BYTE("PRIVMSG %s :%s" % (recipient, message))
	elif (mode == 1):
		return BYTE("NOTICE %s :%s" % (recipient, message))
	else:
		print("Unrecognized mode. Not sending message.")

def getUser(token):
	user = token[0].strip(":")
	user = user.split("!")[0]
	user = user.split("|")[0]
	return user

def getMessage(tokens, startingIndex = 3):
	message = ""
	for i in range(startingIndex, len(tokens)):
		if (i == startingIndex):
			tokens[i] = tokens[i].strip(":")
		message += tokens[i].strip("\x01") + " "
	return message


class PluginBot(threading.Thread):
	userInput = None
	s = None
	focusedChannel = ""
	channels = []
	loadedModules = []
	isRunning = False

	def __init__(self):
		super().__init__()
		print()
		print("┌------------------------------------┐")
		print("|   IRC Client + Plugins Bot  v1.0   |")
		print("└------------------------------------┘")
		print()
		self.userInput = UserInput.UserInput(self)
		self.loadPlugins()
		atexit.register(self.quit)

	def connect(self):
		host = "chat.freenode.net" #"irc.rizon.net"
		port = 6667 #random.randrange(6667, 6669)
		self.focusedChannel = "#wedrbot"
		realName = "WedrPython3Bot"
		identify = "a1b2c3d4"
		nickName = "WedrBot"
		self.channels.clear()

		if (self.s == None):
			self.s = socket.socket()
		print("Connecting to host \"%s\" with port %d." % (host, port))
		self.s.connect((host, port))
		sleep(0.5)
		print("Starting bot main thread.")
		self.start()
		sleep(0.5)
		print("Setting mode for %s" % (realName))
		self.s.send(BYTE("USER %s %s unused :%s" % (identify, host, realName)))
		sleep(0.5)
		print("Logging in using nickname.")
		self.s.send(BYTE("NICK %s" % nickName))
		sleep(0.5)
		print("Identifying...")
		self.s.send(BYTE("PRIVMSG NickServ :identify %s" % identify))
		sleep(0.5)
		print("Joining %s" % self.focusedChannel)
		self.s.send(BYTE("JOIN %s" % self.focusedChannel))
		self.channels.append(self.focusedChannel)
		sleep(0.5)
		print("Requesting Verbose mode.")
		self.s.send(BYTE("PRIVMSG NickServ identify %s" % identify))
		sleep(0.5)
		print("You can now type inside this command prompt/terminal.")
		print("Type \"/help\" for all bot commands.")
		print()
		print("--------------------------------------")
		print()

	def loadPlugins(self):
		print("Loading plugins from /plugins folder:")
		directory = os.getcwd()
		pluginFiles = next(os.walk(directory + "/plugins"))[2]
		self.loadedModules.clear()
		for i in range(len(pluginFiles)):
			name = pluginFiles[i]
			if (name == "template.py"):
				continue
			module = self.loadModule(str("plugins." + pluginFiles[i])[:-3])
			if (module != ""):
				self.loadedModules.append((name, module))
			else:
				print(" --- %s - Invalid plugin." % name)
		for i in range(len(self.loadedModules)):
			print(" --- %s" % self.loadedModules[i][1].version())
		print()
		print("--------------------------------------")
		print()

	def loadModule(self, name):
		temp = importlib.import_module(name)
		if ("version" in dir(temp) and "plugin_main" in dir(temp)):
			return temp
		return ""

	def reloadAll(self):
		print("Reloading plugin")
		for i in range(len(self.loadedModules)):
			self.loadedModules[i] = (self.loadedModules[i][0], importlib.reload(self.loadedModules[i][1]))
		directory = os.getcwd()
		pluginFiles = next(os.walk(directory + "/plugins"))[2]
		for i in range(len(pluginFiles)):
			name = pluginFiles[i]
			if (name == "template.py"):
				continue
			if (any(name in sub for sub in self.loadedModules)):
				continue
			module = self.loadModule(str("plugins." + pluginFiles[i])[:-3])
			if (module != ""):
				self.loadedModules.append((name, module))
			else:
				print(" --- %s - Invalid plugin." % name)
		for i in range(len(self.loadedModules)):
			print(" --- %s" % self.loadedModules[i][1].version())
		print()
		print("--------------------------------------")
		print()


	def quit(self):
		print("Quitting by closing window.")
		if (self.s != None):
			while (len(self.channels) > 0):
				self.s.send(BYTE("PART %s [Bot has left the scene.]" % self.channels[len(self.channels)-1]))
				self.channels.pop()
			self.s.send(BYTE("QUIT %s" % "Test"))
		self.isRunning = False

	def switch(self, newChannel):
		if (newChannel[0] != "#"):
			newChannel = "#%s" % newChannel
		checkFlag = False
		for chan in self.channels:
			if (chan == newChannel):
				checkFlag = True;
				break
		if (checkFlag):
			print("Switching to channel %s" % newChannel)
			self.focusedChannel = newChannel
		else:
			print("Joining and switching to channel %s" % newChannel)
			if (self.s != None):
				self.s.send(BYTE("JOIN %s" % newChannel))
			self.channels.append(newChannel)
			self.focusedChannel = newChannel

	def run(self):
		self.isRunning = True
		readBuffer = ""
		while (self.isRunning):
			try:
				if (self.s != None):
					temp = self.s.recv(1024).decode("UTF-8")
					if (temp == ""):
						self.isRunning = False
					else:
						readBuffer += temp
						temp = readBuffer.split("\n")
						readBuffer = temp.pop()
						for line in temp:
							line = line.rstrip()
							tokens = line.split(" ")
							self.handleTokens(tokens)
			except Exception:
				traceback.print_tb(sys.exc_info()[2])
		print("Closing socket...")
		self.s.shutdown(socket.SHUT_RDWR)
		sleep(0.5)
		self.s.close()
		atexit.unregister(self.quit)

	def handleTokens(self, tokens):
		for i in range(len(self.loadedModules)):
			if ("plugin_main" in dir(self.loadedModules[i][1])):
				self.loadedModules[i][1].plugin_main(self, tokens)

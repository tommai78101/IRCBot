import os
import random
import socket
import string
import importlib
import atexit
from time import sleep

import UserInput

global DEBUG
DEBUG = True

def BYTE(message):
	return bytes("%s\r\n" % message, "UTF-8")


class PluginBot:
	userInput = None
	s = None
	channel = ""
	channels = []
	loadedModules = []
	isRunning = False

	def __init__(self):
		self.userInput = UserInput.UserInput(self)
		self.connect()
		self.loadPlugins()
		self.isRunning = False
		atexit.register(self.quit)

	def connect(self):
		host = "irc.rizon.net"
		port = random.randrange(6667, 6669)
		self.channel = "#wedrbot" if DEBUG else "#3dshacks"
		realName = "WedrPython3Bot"
		identify = "a1b2c3d4"
		nickName = "WedrBot"
		self.channels.clear()

		if (self.s == None):
			self.s = socket.socket()
		print("Connecting to host \"%s\" with port %d." % (host, port))
		self.s.connect((host, port))
		sleep(0.2)
		print("Identifying as %s" % (realName))
		self.s.send(BYTE("USER %s %s unused :%s" % (identify, host, realName)))
		sleep(0.2)
		print("Logging in using nickname.")
		self.s.send(BYTE("NICK %s" % nickName))
		sleep(0.2)
		print("Joining %s" % self.channel)
		self.s.send(BYTE("JOIN %s" % self.channel))
		self.channels.append(self.channel)
		sleep(0.2)
		print("Requesting Verbose mode.")
		self.s.send(BYTE("PRIVMSG NickServ identify %s" % identify))
		sleep(0.2)

	def loadPlugins(self):
		directory = os.getcwd()
		pluginFiles = next(os.walk(directory + "/plugins"))[2]
		self.loadedModules.clear()
		for i in range(len(pluginFiles)):
			name = pluginFiles
			module = self.loadModule(str("plugins." + pluginFiles[i])[:-3])
			self.loadedModules.append((name, module))
			print("Loaded plugin %s successfully." % name)

	def loadModule(self, name):
		return importlib.import_module(name)

	def reloadAll(self):
		for i in range(len(self.loadedModules)):
			print("Reloading plugin")
			self.loadedModules[i] = (self.loadedModules[i][0], importlib.reload(self.loadedModules[i][1]))

	def quit(self):
		print("Quitting by closing window.")
		self.s.send(BYTE("PART %s Bot has left the scene.\r\n" % self.channel))
		self.s.send(BYTE("QUIT %s\r\n" % "Test"))

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
			self.channel = newChannel
		else:
			print("Joining and switching to channel %s" % newChannel)
			self.s.send(BYTE("JOIN %s" % newChannel))
			self.channels.append(newChannel)
			self.channel = newChannel

	def run(self):
		self.isRunning = True
		readBuffer = ""
		while (self.isRunning):
			try:
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
			except Exception as error:
				print("PluginBot Error: ", error)

	def handleTokens(self, tokens):
		for i in range(len(self.loadedModules)):
			if ("plugin_main" in dir(self.loadedModules[i][1])):
				self.loadedModules[i][1].plugin_main(self.s, self.channel, tokens)

def main():
	bot = PluginBot()
	bot.run()
	bot.userInput.join()
	

if __name__ == "__main__":
	main()
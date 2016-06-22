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
	return user

def getMessage(tokens, startingIndex = 3):
	message = ""
	for i in range(startingIndex, len(tokens)):
		message += tokens[i].strip("\x01") + " "
	return message


class PluginBot(threading.Thread):
	userInput = None
	s = None
	focusedChannel = "#wedrbot"
	channels = []
	loadedModules = dict()
	isRunning = False
	guiParent = None
	realName = "WedrPython3Bot"
	password = "a1b2c3d4"
	nickName = "WedrClient"
	host = "irc.rizon.net" #"chat.freenode.net" #
	port = random.randrange(6660, 6669)
	master = "wedr"

	def __init__(self, gui = None):
		super().__init__()
		if (gui != None):
			self.guiParent = gui
			self.guiParent.print()
			self.guiParent.print("┌------------------------------------┐")
			self.guiParent.print("|   IRC Client + Plugins Bot  v1.0   |")
			self.guiParent.print("└------------------------------------┘")
			self.guiParent.print()
		else:
			print()
			print("┌------------------------------------┐")
			print("|   IRC Client + Plugins Bot  v1.0   |")
			print("└------------------------------------┘")
			print()

		self.reloadAll()
		if (self.guiParent == None):
			self.userInput = UserInput.UserInput(self)
		atexit.register(self.quit)

	def connect(self):
		self.channels.clear()

		if (self.s == None):
			self.s = socket.socket()

		if (self.guiParent != None):
			self.guiParent.print("Connecting to host \"%s\" with port %d." % (self.host, self.port))
		else:
			print("Connecting to host \"%s\" with port %d." % (self.host, self.port))
		self.s.connect((self.host, self.port))
		sleep(0.5)

		if (self.guiParent != None):
			self.guiParent.print("Setting mode for %s" % (self.realName))
		else:
			print("Setting mode for %s" % (self.realName))
		self.s.send(BYTE("USER %s %s unused :%s" % (self.password, self.host, self.realName)))
		sleep(0.5)

		if (self.guiParent != None):
			self.guiParent.print("Logging in using nickname.")
		else:
			print("Logging in using nickname.")
		self.s.send(BYTE("NICK %s" % self.nickName))
		sleep(0.5)

		if (self.guiParent != None):
			self.guiParent.print("Starting bot thread.")
		else:
			print("Starting bot thread.")
			self.start()
			sleep(0.5)

		if (self.guiParent != None):
			self.guiParent.print("You can now type inside this command prompt/terminal.")
			self.guiParent.print("Type \"/help\" for all bot commands.")
			self.guiParent.print()
			self.guiParent.print("--------------------------------------")
			self.guiParent.print()
		else:
			print("You can now type inside this command prompt/terminal.")
			print("Type \"/help\" for all bot commands.")
			print()
			print("--------------------------------------")
			print()

	def loadModule(self, name):
		temp = importlib.import_module(name)
		if ("version" in dir(temp) and "plugin_main" in dir(temp)):
			return temp
		return ""

	def identify(self):
		if (self.guiParent != None):
			self.guiParent.print("Identifying...")
		else:
			print("Identifying...")
		self.s.send(BYTE("USER %s %s unused :%s" % (self.password, self.host, self.realName)))
		sleep(0.5)
		self.s.send(BYTE("PRIVMSG NickServ :identify %s" % self.password))
		sleep(0.5)

	def reloadAll(self):
		if (self.guiParent != None):
			self.guiParent.print()
			self.guiParent.print("Reloading plugin")
		else:
			print()
			print("Reloading plugin")
		directory = os.getcwd()
		pluginFiles = next(os.walk(directory + "/plugins"))[2]
		if (len(pluginFiles) > len(self.loadedModules)):
			for i in range(len(pluginFiles)):
				name = pluginFiles[i]
				if (name == "template.py"):
					continue
				if (name in self.loadedModules and name in pluginFiles):
					self.loadedModules[name] = importlib.reload(self.loadedModules[name])
				elif (name in self.loadedModules and not name in pluginFiles):
					del self.loadedModules[name]
				else:
					module = self.loadModule(str("plugins." + name)[:-3])
					if (module != ""):
						self.loadedModules[name] = module
					else:
						if (self.guiParent != None):
							self.guiParent.print(" --- %s - Invalid plugin." % name)
						else:
							print(" --- %s - Invalid plugin." % name)
		else:
			tempList = []
			for i in self.loadedModules:
				check = False
				for name in pluginFiles:
					if (i == name and name != "template.py"):
						check = True
						break
				if (check):
					self.loadedModules[i] = importlib.reload(self.loadedModules[i])
				else:
					tempList.append(i)
			for i in tempList:
				del self.loadedModules[i]
					

		for i in self.loadedModules:
			if (self.guiParent != None):
				self.guiParent.print(" --- %s" % self.loadedModules[i].version())
			else:
				print(" --- %s" % self.loadedModules[i].version())

		if (self.guiParent != None):
			self.guiParent.print()
			self.guiParent.print("--------------------------------------")
			self.guiParent.print()
		else:
			print()
			print("--------------------------------------")
			print()


	def quit(self):
		print("Quitting by closing window.")
		if (self.s != None):
			while (len(self.channels) > 0):
				self.s.send(BYTE("PART %s :[Bot has left the scene.]" % self.channels[len(self.channels)-1]))
				self.channels.pop()
			self.s.send(BYTE("QUIT %s :%s" % ("Test", "Hello world.")))
		self.isRunning = False

	def leave(self, channel, isKicked):
		if (channel in self.channels):
			if (isKicked):
				self.s.send(BYTE("PART %s :%s" % (channel, "I am leaving.")))
			self.channels.remove(channel)
			if (self.guiParent != None):
				self.guiParent.print("Bot left the channel, %s" % channel)
			else:
				print("Bot left the channel, %s" % channel)
			return True
		else:
			if (self.guiParent != None):
				self.guiParent.print("Channel, %s, does not exist." % channel)
			else:
				print("Channel, %s, does not exist." % channel)
			return False

	def switch(self, newChannel, isJoining = True):
		if (newChannel != "" and newChannel[0] != "#"):
			newChannel = "#%s" % newChannel
		checkFlag = False
		self.focusedChannel = ""
		if (not isJoining):
			return
		for chan in self.channels:
			if (chan == newChannel):
				checkFlag = True;
				break
		if (checkFlag):
			if (self.guiParent != None):
				self.guiParent.print("Switching to channel %s" % newChannel)
			else:
				print("Switching to channel %s" % newChannel)
			self.focusedChannel = newChannel
		else:
			if (self.guiParent != None):
				self.guiParent.print("Joining and switching to channel %s" % newChannel)
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
							self.handleTokens(self.makeTokens(line))
			except Exception:
				traceback.print_tb(sys.exc_info()[2])
		print("Closing socket...")
		self.s.shutdown(socket.SHUT_RDWR)
		sleep(0.5)
		self.s.close()
		atexit.unregister(self.quit)

	def makeTokens(self, line):
		line = line.rstrip()
		tokens = line.split(" ")
		tokens[0] = getUser(tokens)
		index = self.getStartingIndex(line)
		if (len(tokens) > index):
			tokens[index] = tokens[index][1:]
		tokens = list(filter(lambda x: x != "", tokens))
		return tokens

	def getStartingIndex(self, tokens):
		startingIndex = 1
		tokens = tokens.split(" ")
		while (startingIndex < len(tokens)-1 and tokens[startingIndex][0] != ":"):
			startingIndex += 1
		return startingIndex

	def handleTokens(self, tokens):
		for i in self.loadedModules:
			if ("plugin_main" in dir(self.loadedModules[i])):
				try:
					self.loadedModules[i].plugin_main(self, tokens)
				except Exception as error:
					print("%s: %s" % (i, error))

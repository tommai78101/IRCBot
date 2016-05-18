﻿import sys
import socket
import string
from datetime import datetime
import threading


def BYTE(message):
	return bytes(message, "UTF-8")

class IRCBot:
	host = ""
	port = 0
	s = None
	identify = "a1b2c3d4"
	nickName = "WedrBot"
	realName = "WedrPython3Bot"
	master = "wedr"
	email = "wedr53-trash@yahoo.com.tw"
	channel = ""
	joinedChannels = []
	quitFlag = False
	readBuffer = ""
	currentDate = datetime.now()
	userInput = None

	def __init__(self, host, port, channel):
		self.host = host
		self.port = port
		self.channel = channel
		self.quitFlag = False
		self.userInput = self.UserInput(self)

	#def setChannels(self, channels):
	#	self.channel = channels

	def connect(self):
		if (self.s == None):
			self.s = socket.socket()
		print("Connecting to host: %s:%s" % (self.host, self.port))
		self.s.connect((self.host, self.port))
		print("Identifying as %s." % self.realName)
		self.s.send(BYTE("USER %s %s bla :%s\r\n" % (self.identify, self.host, self.realName)))
		print("Logging in as %s" % self.nickName)
		self.s.send(BYTE("NICK %s\r\n" % self.nickName))
		#if (len(self.channel) > 1):
		#	print("Joining the list of channels: %s" % self.channel)
		#	for chan in self.channel:
		#		self.s.send(BYTE("JOIN %s\r\n" % chan))
		#else:
		print("Joining %s" % self.channel)
		self.s.send(BYTE("JOIN %s\r\n" % self.channel))
		self.switchAndJoinChannel(self.channel)
		print("Adding channel to joined list.")

	def sendMessage(self, recipient, message, mode):
		if (mode == 0):
			self.s.send(BYTE("PRIVMSG %s :%s\r\n" % (recipient, message)))
		elif (mode == 1):
			self.s.send(BYTE("NOTICE %s :%s\r\n" % (recipient, message)))
		elif (mode == 2):
			self.s.send(BYTE("PRIVMSG %s :\x01ACTION %s\x01\r\n" % (recipient, message)))

	def handleTokens(self, tokens):
		#PING protocol
		#tokens[0] is the command, which is PING.
		#tokens[1] is the sender.
		#PING requires the bot to return PONG.
		if (tokens[0] == "PING"):
			self.currentDate = datetime.now()
			print("[%02s:%02s] Received PING PONG" % (str(self.currentDate.hour).zfill(2), str(self.currentDate.minute).zfill(2)))
			str1 = ("PONG %s\r\n" % tokens[1].strip(":"))
			self.s.send(BYTE(str1))

		#PRIVMSG protocol
		#tokens[0] gets the full user account. This needs to be stripped and splitted out.
		#tokens[1] is the command. PRIVMSG is a command.
		#tokens[2] is the channel or recipient name.
		#tokens[3] is the full message with a leading colon. This needs to be stripped.
		if (len(tokens) > 1 and tokens[1] == "PRIVMSG"):
			if (len(tokens) > 2 and tokens[3] == ":\x01VERSION\x01"):
				print("Sending VERSION")
				self.s.send(BYTE("NOTICE %s :\x01VERSION WedrBot v1.0\x01" % tokens[0]))
				self.sendMessage("NickServ", "identify a1b2c3d4", 0)
				self.switchAndJoinChannel(self.channel)
				self.sendMessage("wedr", "Hello world.", 0)
				if (self.userInput.isStarting != True):
					print("Starting Input thread.")
					self.userInput.start()
			else:
				caller = self.getUser(tokens[0])
				message = self.getMessage(tokens, 3)
				if (caller == "wedr" and message.rstrip() == ".quitBot"):
					print("Quitting...")
					self.quitFlag = True
					return
				recipient = tokens[2]
				try:
					print("%s: %s" % (caller, message))
					self.handlePrivateMessage(caller, recipient, message)
				except NotImplementedError as error:
					print("Error was thrown : %s" % error)
					return

	def handlePrivateMessage(self, user, recipient, message):
		raise NotImplementedError("Subclass must implement this.")

	def switchAndJoinChannel(self, channel):
		if (channel[0] == "#"):
			checkFlag = False
			for joined in self.joinedChannels:
				if (channel == joined):
					checkFlag = True
					break
			if (checkFlag):
				self.channel = channel
			else:
				self.joinedChannels.append(channel)
				self.s.send(BYTE("JOIN %s\r\n" % channel))
				self.sendMessage("NickServ", "identify a1b2c3d4", 0)
				self.channel = channel
		else:
			print("Usage: /switch [CHANNEL TO SPEAK IN] - And make sure you type in the number sign.")

	def getUser(self, token):
		user = token.strip(":")
		user = user.split("!")[0]
		return user

	def getMessage(self, tokens, startingIndex):
		message = ""
		for i in range(startingIndex, len(tokens)):
			if (i == startingIndex):
				tokens[i] = tokens[i].strip(":")
			message += tokens[i].strip("\x01") + " "
		return message

	def run(self):
		while not (self.quitFlag):
			readBuffer = ""
			try:
				readBuffer += self.s.recv(1024).decode("UTF-8")
				temp = str.split(readBuffer, "\n")
				readBuffer = temp.pop()
				for line in temp:
					line = line.rstrip()
					tokens = line.split(" ")
					self.handleTokens(tokens)
			except Exception as error:
				print("Bot encountered an error. Quitting...")
				print("Error message: %s" % str(error))
				#self.quitFlag = True

	class UserInput(threading.Thread):
		parent = None
		isStarting = False

		def __init__(self, parent):
			threading.Thread.__init__(self)
			self.parent = parent
			self.isStarting = False
			print("Initializing input.")
		
		def run(self):
			self.isStarting = True
			while (self.parent.quitFlag != True):
				try:
					message = input()
					message = message.split(" ")
					if (message[0] == "/msg"):
						messageEnd = ""
						for i in range(2, len(message)):
							messageEnd += message[i] + " "
						self.parent.sendMessage(message[1], messageEnd, 0)
					elif (message[0] == "/me"):
						messageEnd = ""
						for i in range(1, len(message)):
							messageEnd += message[i] + " "
						self.parent.sendMessage(self.parent.channel, messageEnd, 2)
					elif (message[0] == "/j"):
						messageEnd = ""
						for i in range(1, len(message)):
							messageEnd += message[i] + " "
						messageEnd = messageEnd.split(" ")
						messageEnd.pop()
						if (len(messageEnd) > 1):
							for chans in messageEnd:
								self.parent.s.send(BYTE("JOIN %s\r\n" % chans))
								self.parent.sendMessage("NickServ", "identify a1b2c3d4", 0)
								if (chans[0] != "#"):
									chans.insert(0, "#")
								checkFlag = False
								for check in self.parent.joinedChannels:
									if (check == chans):
										checkFlag = True
										break
								if (not checkFlag):
									self.parent.joinedChannels.append(chans)
							print("Remember to /switch to the new channel to speak there.")
						else:
							if (messageEnd[0][0] != "#"):
								messageEnd[0] = "#%s" % messageEnd[0]
							self.parent.s.send(BYTE("JOIN %s\r\n" % messageEnd[0]))
							self.parent.sendMessage("NickServ", "identify a1b2c3d4", 0)
							print("Joining channel: %s" % messageEnd[0])
							self.parent.switchAndJoinChannel(messageEnd[0])
					elif (message[0] == "/switch"):
						self.parent.switchChannel(message)
					elif (message != [""]):
						messageEnd = ""
						for i in range(0, len(message)):
							messageEnd += message[i] + " " 
						self.parent.sendMessage(self.parent.channel, messageEnd, 0)
				except Exception as error:
					print(error)

				

	
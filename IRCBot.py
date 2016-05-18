import sys
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
		self.joinedChannels.append(self.channel)
		print("Adding channel to joined list.")

	def sendMessage(self, recipient, message, mode):
		if (mode == 0):
			self.s.send(BYTE("PRIVMSG %s :%s\r\n" % (recipient, message)))
		elif (mode == 1):
			self.s.send(BYTE("NOTICE %s :%s\r\n" % (recipient, message)))
		elif (mode == 2):
			self.s.send(BYTE("PRIVMSG %s :\x01ACTION %s\x01\r\n" % (recipient, message)))

	def handleTokens(self, tokens):
		#print(tokens)

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
				self.sendMessage("NickServ", "identify a1b2c3d4", 0)
				self.s.send(BYTE("JOIN %s\r\n" % self.channel))
				self.sendMessage("wedr", "Hello world.", 1)
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

	def getUser(self, token):
		user = token.strip(":")
		user = user.split("!")[0]
		return user

	def getMessage(self, tokens, startingIndex):
		message = ""
		for i in range(startingIndex, len(tokens)):
			if (i == startingIndex):
				tokens[i] = tokens[i].strip(":")
			message += str(tokens[i]).strip("\x01") + " "
		return message

	def run(self):
		self.sendMessage("wedr", "Hello world. Where am I?", 1)
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

		def __init__(self, parent):
			threading.Thread.__init__(self)
			self.parent = parent
			print("Initializing input.")
		
		def run(self):
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
						if (len(messageEnd.split(" ")) > 1):
							for j in range(1, len(message)):
								self.parent.s.send(BYTE("JOIN %s\r\n" % message[i]))
								self.parent.sendMessage("NickServ", "identify a1b2c3d4", 0)
								if (message[i][0] != "#"):
									message[i].insert(0, "#")
								self.parent.joinedChannels.append(message[i])
						else:
							self.parent.s.send(BYTE("JOIN %s\r\n" % messageEnd))
							self.parent.sendMessage("NickServ", "identify a1b2c3d4", 0)
							if (messageEnd[0] != "#"):
									messageEnd.insert(0, "#")
							self.parent.joinedChannels.append(messageEnd)
						print("Remember to /switch to the new channel to speak there.")
					elif (message[0] == "/switch"):
						if (len(message) == 2):
							channelName = message[1]
							checkFlag = False
							for joined in self.parent.joinedChannels:
								if (channelName == joined):
									checkFlag = True
									break
							if (checkFlag):
								self.parent.channel = message[1]
						else:
							print("Usage: /switch [CHANNEL TO SPEAK IN] - And make sure you type in the number sign.")
					elif (message != [""]):
						messageEnd = ""
						for i in range(0, len(message)):
							messageEnd += message[i] + " "
						self.parent.sendMessage(self.parent.channel, messageEnd, 0)
				except Exception as error:
					print(error)

				

	
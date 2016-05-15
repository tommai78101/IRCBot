import sys
import socket
import string
from datetime import datetime

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
	quitFlag = False
	readBuffer = ""
	currentDate = datetime.now()

	def __init__(self, host, port, channel):
		self.host = host
		self.port = port
		self.channel = channel
		self.quitFlag = False

	def connect(self):
		if (self.s == None):
			self.s = socket.socket()
		print("Connecting to host: %s:%s" % (self.host, self.port))
		self.s.connect((self.host, self.port))
		print("Identifying as %s." % self.realName)
		self.s.send(BYTE("USER %s %s bla :%s\r\n" % (self.identify, self.host, self.realName)))
		print("Logging in as %s" % self.nickName)
		self.s.send(BYTE("NICK %s\r\n" % self.nickName))
		print("Joining %s" % self.channel)
		self.s.send(BYTE("JOIN %s\r\n" % self.channel))

	def sendMessage(self, recipient, message):
		self.s.send(BYTE("PRIVMSG %s :%s\r\n" % (recipient, message)))

	def handleTokens(self, tokens):
		#PING protocol
		#tokens[0] is the command, which is PING.
		#tokens[1] is the sender.
		#PING requires the bot to return PONG.
		if (tokens[0] == "PING"):
			self.currentDate = datetime.now()
			print("[%02s:%02s] Received PING PONG" % (str(self.currentDate.hour).zfill(2), str(self.currentDate.minute).zfill(2)))
			self.s.send(BYTE("PONG %s\r\n" % tokens[1]))
			return

		#PRIVMSG protocol
		#tokens[0] gets the full user account. This needs to be stripped and splitted out.
		#tokens[1] is the command. PRIVMSG is a command.
		#tokens[2] is the channel or recipient name.
		#tokens[3] is the full message with a leading colon. This needs to be stripped.
		if (len(tokens) > 1 and tokens[1] == "PRIVMSG"):
			caller = self.getUser(tokens[0])
			message = self.getMessage(tokens, 3)
			if (caller == "wedr" and message.rstrip() == ".quitBot"):
				print("Quitting...")
				self.quitFlag = True
				return
			recipient = tokens[2]
			try:
				print("Handling message from %s: %s" % (caller, message))
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
		self.sendMessage("wedr", "Hello world.")
		while not (self.quitFlag):
			try:
				readBuffer = self.s.recv(1024).decode("UTF-8")
				temp = str.split(readBuffer, "\n")
				readBuffer = temp.pop()
				for line in temp:
					line = line.rstrip()
					tokens = line.split(" ")
					self.handleTokens(tokens)
			except Exception as error:
				print("Bot encountered an error. Quitting...")
				print("Error message: %s" % str(error))
				self.quitFlag = True

				

	
import os
import string
import atexit
from IRCBot import IRCBot
from IRCBot_updates import UpdateBot
from IRCBot_quotes import QuotesBot

global FILE_SEPARATOR
FILE_SEPARATOR = "\\"

class FilesBot(QuotesBot):
	saveFileName = "quote"
	temp = "quote.tmp"
	saveFilePath = ""

	def __init__(self, host, port, channel):
		super().__init__(host, port, channel)
		self.saveFilePath = os.getcwd()
		self.load(0)
		atexit.register(save, mode = 0)

	def createTempFile(self):
		file = open(self.saveFilePath + FILE_SEPARATOR + self.temp, "wb")
		file.write("".encode())

	def openTempFile(self):
		return open(self.saveFilePath + FILE_SEPARATOR + self.temp, "ab")

	def save(self, mode):
		self.createTempFile()
		file = self.openTempFile()
		#Quotes = 0
		try:
			if (mode == 0):
				with file as f:
					for line in self.quotes:
						temp = "%s%s" % (line.encode(), "\n")
						f.write(line.encode())
		finally:
			if (file != None):
				file.close()
				file = None
		os.replace(self.saveFilePath + FILE_SEPARATOR + self.temp, self.saveFilePath + FILE_SEPARATOR + self.saveFileName)

	def load(self, mode):
		if (mode == 0):
			file = None
			try:
				file = open(self.saveFilePath + FILE_SEPARATOR + self.saveFileName, "rb")
				with file as f:
					self.quotes.clear()
					f.seek(0)
					for line in file:
						temp = line.decode()
						if (temp != "\n"):
							self.quotes.append(temp)
			except:
				if (file != None):
					file.close()
					file = None
			finally:
				if (file != None):
					file.close()
					file = None

	def handlePrivateMessage(self, user, recipient, message):
		super().handlePrivateMessage(user, recipient, message)
		messageTokens = message.strip().split(" ")
		if (messageTokens[0] == ".wedr" and len(messageTokens) == 2):
			if (messageTokens[1] == "help"):
				self.sendMessage(user, ".wedr save - Saves the Quotes List.", 1)
				self.sendMessage(user, ".wedr load - Loads the Quotes List.", 1)
			elif (messageTokens[1] == "save"):
				try:
					self.save(0)
					print("Quotes List saved.")
					self.sendMessage(self.channel, "Quotes List saved.", 0)
				except Exception as error:
					print("Unable to save - %s" % (str(error)))
					self.sendMessage(self.channel, "Unable to save. Please notify " + self.master + " to fix this issue.", 0)
			elif (messageTokens[1] == "load"):
				try:
					self.load(0)
					print("Quotes List loaded...")
					self.sendMessage(self.channel, "Quotes List loaded.", 0)
				except Exception as error:
					print("Unable to load - %s" % (str(error)))
					self.sendMessage(self.channel, "Unable to load. Please notify " + self.master + " to fix this issue.", 0)








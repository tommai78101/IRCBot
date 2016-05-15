import os
import string
from IRCBot_updates import UpdateBot

class QuotesBot(UpdateBot):
	quotes = []
	saveFileName = "quotes.txt"
	saveFile = None

	def __init__(self, host, port, channel):
		super().__init__(host, port, channel)

	def handlePrivateMessage(self, user, recipient, message):
		super().handlePrivateMessage(user, recipient, message);
		messageTokens = message.strip().split(" ")
		if (messageTokens[0] == ".quote"):
			if (len(messageTokens) >= 2):
				if (messageTokens[1] == "add"):
					if (len(messageTokens) > 2):
						tempString = ""
						for i in range(2, len(messageTokens)):
							tempString += messageTokens[i] + " "
						self.quotes.append("[%s] %s" % (user, tempString))
						print("Quote has been added.")
						self.sendMessage(self.channel, "Quote added.")
					else:
						self.sendMessage(self.channel, ".quote add <MESSAGE> - Add MESSAGE to Quotes List.")
				elif (messageTokens[1].isnumeric()):
					try:
						quoteIndex = int(messageTokens[1])
						if (quoteIndex > len(self.quotes) or quoteIndex <= 0):
							print("Index is invalid.")
							self.sendMessage(self.channel, "Invalid quote index. Enter number from 1 to current size of Quotes List.")
						else:
							print("Showing quote #%s" % (str(self.quotes[quoteIndex - 1])))
							self.sendMessage(self.channel, "Quote #%s: %s" % (str(quoteIndex), str(self.quotes[quoteIndex - 1])))
					except ValueError:
						print("Error converting string to integer.")
					except Exception as error:
						print("Error - %s" % (str(error)))
				elif (messageTokens[1] == "remove" and len(messageTokens) > 2 and messageTokens[2].isnumeric()):
					try:
						quoteIndex = int(messageTokens[2])
						if (quoteIndex > len(self.quotes) or quoteIndex <= 0):
							print("Index is invalid.")
							self.sendMessage(self.channel, "Invalid quote index. Enter number from 1 to current size of Quotes List.")
						else:
							self.quotes.remove(self.quotes[quoteIndex - 1])
							print("Successfully removed quote #%s" % (messageTokens[2]))
							self.sendMessage(self.channel, "Quote #%s has been removed." % (messageTokens[2]))
					except Exception:
						print("Quote #%s does not exist." % (messageTokens[2]))
						self.sendMessage(self.channel, "Quote #%s does not exist." % (messageTokens[2]))
				elif (messageTokens[1] == "capacity" or messageTokens[1] == "size"):
					print("Showing quotes list size.")
					self.sendMessage(self.channel, "Quotes List size : %s" % (str(len(self.quotes))))
				elif (messageTokens[1] == "help"):
					self.sendMessage(self.channel, ".quote add <MESSAGE> - Add MESSAGE to Quotes List.")
					self.sendMessage(self.channel, ".quote remove <INDEX> - Removes quote from Quotes List.")
					self.sendMessage(self.channel, ".quote <INDEX> - Outputs quote from Quotes List.")
					self.sendMessage(self.channel, ".quote size - Outputs quote list size from Quotes List.")
					self.sendMessage(self.channel, ".quote capacity - Outputs quote list size from Quotes List.")
					self.sendMessage(self.channel, ".quote help - Brings up all commands and descriptions.")
				#elif (messageTokens[1] == "save"):
				#	self.saveFile = open(os.getcwd() + "\\" + self.saveFileName, "rwb")

		elif (messageTokens[0] == ".help"):
			self.sendMessage(self.channel, ".quote <Command> - Type \".quote help\" for more info.")

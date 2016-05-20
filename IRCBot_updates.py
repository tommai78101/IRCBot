import sys
import socket
from urllib import request
from IRCBot import IRCBot
from inspect import currentframe, getframeinfo

class UpdateBot(IRCBot):
	csv_old3DS = "https://yls8.mtheall.com/ninupdates/titlelist.php?sys=ctr&csv=1"
	csv_new3DS = "https://yls8.mtheall.com/ninupdates/titlelist.php?sys=ktr&csv=1"

	def __init__(self, host, port, channel):
		super().__init__(host, port, channel)


	def handlePrivateMessage(self, user, recipient, message):
		#There's no need to call on super(), because the base class contains the virtual method for this method.
		messageTokens = message.split(" ")
		messageTokens.pop()
		temp = messageTokens[0].lower()
		if (temp == ".lookforupdate" or temp == ".lfu"):
			if (len(messageTokens) == 3):
				if (len(messageTokens[1]) == 16):
					try:
						self.getRequiredUpdates(user, messageTokens, True)
						self.getRequiredUpdates(user, messageTokens, False)
					except Exception as error:
						frameinfo = getframeinfo(currentframe())
						print("Cannot parse update list... : [%s, %s] %s" % (str(frameinfo.filename).split("\\").pop(), frameinfo.lineno, str(error)))
						self.sendMessage(self.channel, "Unable to parse update list... : [%s, %s] %s" % (str(frameinfo.filename).split("\\").pop(), frameinfo.lineno, str(error)), 0)
				else:
					self.sendMessage(user, "Incorrect Title ID.", 1)
			else:
				self.sendMessage(self.channel, ".lookforupdate [Title ID] [Region] -OR- .lfu [Title ID] [Region] - Returns Firmware Versions Required if exists.", 0)
		elif (temp == ".help"):
			self.sendMessage(user, ".lookforupdate [Title ID] [Region] -OR- .lfu [Title ID] [Region] - Returns Firmware Versions Required if exists.", 1)
			self.sendMessage(user, ".explain - Returns explanation of WedrBot.", 1)
		elif (temp == ".explain"):
			self.sendMessage(user, "Purpose: WedrBot is created in Python 3, for the only sole purpose of practicing Python 3 programming.", 1)
			self.sendMessage(user, "Future: If anyone wishes an IRC bot to do something they desire, please ask the creator, wedr, for suggestions.", 1)

	def parseCSVList(self, csv, user, titleID, region, isOld3DS):
		csvList = csv.split("\n")
		exitNestedLoop = False
		if (len(csvList) > 1):
			for line in csvList:
				if (exitNestedLoop):
					break
				lineTokens = line.split(",")
				if (lineTokens[0][0:4] == "0004" and lineTokens[0] == titleID and lineTokens[1] == region):
					for index in range(2, len(lineTokens)):
						if (lineTokens[index][0] != "v"):
							print("Update(s) for %s : %s" % ("O3DS" if isOld3DS else "N3DS", lineTokens[index]))
							self.sendMessage(self.channel, "Update(s) for %s : %s" % ("O3DS" if isOld3DS else "N3DS", lineTokens[index]), 0)
							return
			print("Failed to locate titleID or region for %s. Required firmware version may not exist." % ("O3DS" if isOld3DS else "N3DS"))
			self.sendMessage(self.channel, "Cannot locate titleID or region for %s. Required firmware version may not exist." % ("O3DS" if isOld3DS else "N3DS"), 0)
		else:
			print("Incorrect CSV List: " + csvList)
			self.sendMessage(user, "This bot encountered a bug. Please report to wedr to fix this.", 1)

	def getRequiredUpdates(self, user, messageTokens, isOld3DS):
		csvList = None
		requestURL = request.Request(self.csv_old3DS if (isOld3DS) else self.csv_new3DS)
		csvList = request.urlopen(requestURL)
		csvList = csvList.read().decode("UTF-8")
		if (csvList != None):
			self.parseCSVList(csvList, user, messageTokens[1], messageTokens[2], isOld3DS)

import socket

from urllib import request
from inspect import currentframe, getframeinfo
from PluginBot import BYTE
from PluginBot import PRIVMSG
from PluginBot import getUser
from PluginBot import getMessage


csv_old3DS = "https://yls8.mtheall.com/ninupdates/titlelist.php?sys=ctr&csv=1"
csv_new3DS = "https://yls8.mtheall.com/ninupdates/titlelist.php?sys=ktr&csv=1"

def parseCSVList(parent, csv, user, titleID, region, isOld3DS):
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
						parent.s.send(PRIVMSG(tokens[2], "Update(s) for %s : %s" % ("O3DS" if isOld3DS else "N3DS", lineTokens[index]), 0))
						return
		print("Failed to locate titleID or region for %s. Required firmware version may not exist." % ("O3DS" if isOld3DS else "N3DS"))
		parent.s.send(PRIVMSG(tokens[2], "Cannot locate titleID or region for %s. Required firmware version may not exist." % ("O3DS" if isOld3DS else "N3DS"), 0))
	else:
		print("Incorrect CSV List: " + csvList)
		parent.s.send(PRIVMSG(user, "This bot encountered a bug. Please report to wedr to fix this.", 1))

def getRequiredUpdates(parent, user, messageTokens, isOld3DS):
	csvList = None
	requestURL = request.Request(csv_old3DS if (isOld3DS) else csv_new3DS)
	csvList = request.urlopen(requestURL)
	csvList = csvList.read().decode("UTF-8")
	if (csvList != None):
		parseCSVList(parent, csvList, user, messageTokens[1], messageTokens[2], isOld3DS)

def handlePrivateMessage(parent, user, message):
	#There's no need to call on super(), because the base class contains the virtual method for this method.
	messageTokens = message.split(" ")
	messageTokens.pop()
	if (len(messageTokens) <= 0):
		return
	temp = messageTokens[0].lower()
	if (temp == ".lookforupdate" or temp == ".lfu"):
		if (len(messageTokens) == 3):
			if (len(messageTokens[1]) == 16):
				try:
					getRequiredUpdates(parent, user, messageTokens, True)
					getRequiredUpdates(parent, user, messageTokens, False)
				except Exception as error:
					frameinfo = getframeinfo(currentframe())
					print("Cannot parse update list... : [%s, %s] %s" % (str(frameinfo.filename).split("\\").pop(), frameinfo.lineno, str(error)))
					parent.s.send(PRIVMSG(tokens[2], "Unable to parse update list... : [%s, %s] %s" % (str(frameinfo.filename).split("\\").pop(), frameinfo.lineno, str(error)), 0))
			else:
				parent.s.send(PRIVMSG(user, "Incorrect Title ID.", 1))
		else:
			parent.s.send(PRIVMSG(tokens[2], ".lookforupdate [Title ID] [Region] -OR- .lfu [Title ID] [Region] - Returns Firmware Versions Required if exists.", 0))
	elif (temp == ".help"):
		parent.s.send(PRIVMSG(user, ".lookforupdate [Title ID] [Region] -OR- .lfu [Title ID] [Region] - Returns Firmware Versions Required if exists.", 1))
		parent.s.send(PRIVMSG(user, ".explain - Returns explanation of WedrBot.", 1))
	elif (temp == ".explain"):
		parent.s.send(PRIVMSG(user, "Purpose: WedrBot is created in Python 3, for the only sole purpose of practicing Python 3 programming.", 1))
		parent.s.send(PRIVMSG(user, "Future: If anyone wishes an IRC bot to do something they desire, please ask the creator, wedr, for suggestions.", 1))

def version():
	return "Updates - v1.0"

def plugin_main(parent, tokens):
	caller = getUser(tokens)
	message = getMessage(tokens, 3)
	handlePrivateMessage(parent, caller, message) 


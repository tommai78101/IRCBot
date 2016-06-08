from PluginBot import BYTE
from PluginBot import PRIVMSG
from PluginBot import getMessage

class AFKList:
	afkList = []

	def addUser(self, parent, channel, user):
		if (not any(a == user for a in self.afkList)):
			self.afkList.append(user)
			parent.s.send(PRIVMSG(channel, "%s has been added to the AFK list." % user, 0))
		else:
			parent.s.send(PRIVMSG(channel, "%s is in the AFK list." % user, 0))

	def removeUser(self, parent, channel, user):
		if (any(a == user for a in self.afkList)):
			self.afkList.remove(user)
			parent.s.send(PRIVMSG(channel, "%s has been removed from the AFK list." % user, 0))
		else:
			parent.s.send(PRIVMSG(channel, "%s is not in the AFK list." % user, 0))


afkObject = AFKList()

def version():
	return "Away From Keyboard - v1.0"

def plugin_main(parent, tokens):
	if ((len(tokens) > 2) and (tokens[2] == "#3dshacks" or tokens[2] == "#3dshacks-ot")):
		return
	if (len(tokens) > 3):
		if (tokens[3] == ".afk"):
			if (len(tokens) > 4):
				if (tokens[4] == "join" or tokens[4] == "j"):
					afkObject.addUser(parent, tokens[2], tokens[0])
				elif (tokens[4] == "leave" or tokens[4] == "l"):
					afkObject.removeUser(parent, tokens[2], tokens[0])
				elif (tokens[4] == "help"):
					parent.s.send(PRIVMSG(tokens[0], "USAGE: .afk join OR .afk j - Get yourself added to the AFK List.", 1))
					parent.s.send(PRIVMSG(tokens[0], "USAGE: .afk leave OR .afk l - Get yourself removed from the AFK List.", 1))
					parent.s.send(PRIVMSG(tokens[0], "USAGE: .afk help - Get all .afk commands.", 1))
				else:
					parent.s.send(PRIVMSG(tokens[2], "Invalid command. Type \".afk help\" for more info.", 0))
			else:
				parent.s.send(PRIVMSG(tokens[2], "Invalid command. Type \".afk help\" for more info.", 0))
		elif (tokens[3] == ".help"):
			parent.s.send(PRIVMSG(tokens[0], "USAGE: .afk help - Get all .afk commands.", 1))
		else:
			message = getMessage(tokens).strip(";:.,\'\"")
			if (any(tokens[0] == a for a in afkObject.afkList)):
				afkObject.removeUser(parent, tokens[2], tokens[0])
			if (any(name in message for name in afkObject.afkList)):
				parent.s.send(PRIVMSG(tokens[0], "I'm sorry, but the user is currently AFK.", 1))



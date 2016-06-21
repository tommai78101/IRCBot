from PluginBot import BYTE
from PluginBot import PRIVMSG
from PluginBot import getMessage

class RIP:
	ripCount = 0
	previousUser = ""
ripObject = RIP()
	
def version():
	if (ripObject != None):
		return "Rest in Peace - v1.0"
	return "ERROR"

def plugin_main(parent, tokens):
	if (len(tokens) > 3):
		if (tokens[3] == ".rip"):
			if (len(tokens) > 4):
				if (tokens[4] == "count"):
					parent.s.send(PRIVMSG(tokens[2], "Total R.I.P. Count: %d" % ripObject.ripCount, 0))
					if (parent.guiParent != None):
						parent.guiParent.print("Total R.I.P. Count: %d" % ripObject.ripCount)
				elif (tokens[4] == "help"):
					parent.s.send(PRIVMSG(tokens[0], "USAGE: .rip - Gives the last spoken user an empathetic message.", 1))
					parent.s.send(PRIVMSG(tokens[0], "USAGE: .rip [USER] - Gives the USER an empathetic message.", 1))
					parent.s.send(PRIVMSG(tokens[0], "USAGE: .rip count - Shows the stats of total number of R.I.P.s.", 1))
					parent.s.send(PRIVMSG(tokens[0], "USAGE: .rip help - Show all .rip commands.", 1))
				else:
					ripObject.previousUser = tokens[4]
					message = getMessage(tokens, 4)
					parent.s.send(PRIVMSG(tokens[2], " -  R.I.P. %s   :(" % message, 0))
					if (parent.guiParent != None):
						parent.guiParent.print(" -  R.I.P. %s   :(" % message)
					ripObject.ripCount += 1
			else:
				if (ripObject.previousUser != ""):
					ripObject.ripCount += 1
					parent.s.send(PRIVMSG(tokens[2], " -  R.I.P. %s   :(" % ripObject.previousUser, 0))
					if (parent.guiParent != None):
						parent.guiParent.print(" -  R.I.P. %s   :(" % ripObject.previousUser)
		elif (tokens[3] == ".help"):
			parent.s.send(PRIVMSG(tokens[0], "USAGE: .rip help - Show all .rip commands.", 1))
		else:
			ripObject.previousUser = tokens[0]
		

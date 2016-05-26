from PluginBot import BYTE
from PluginBot import PRIVMSG

class RIP:
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
				parent.s.send(PRIVMSG(parent.focusedChannel, ".rip - Gives the last spoken user an empathetic message.", 0))
			else:
				if (ripObject.previousUser != ""):
					parent.s.send(PRIVMSG(parent.focusedChannel, " -  R.I.P. %s   :(" % ripObject.previousUser, 0))			
		elif (tokens[3] == ".help"):
			parent.s.send(PRIVMSG(tokens[0], ".rip - Gives the last spoken user an empathetic message.", 1))
			
		else:
			ripObject.previousUser = tokens[0]
		

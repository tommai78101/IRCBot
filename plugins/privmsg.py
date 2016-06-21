import codecs
import tkinter

from PluginBot import BYTE
from PluginBot import PRIVMSG
from PluginBot import getUser
from PluginBot import getMessage

def version():
	codecs.register(lambda name: codecs.lookup("utf-8") if name == "cp65001" else None)
	return "PrivMsg - v1.0"

def plugin_main(parent, tokens):
	#PRIVMSG protocol
	#tokens[0] gets the full user account. This needs to be stripped and splitted out.
	#tokens[1] is the command. PRIVMSG is a command.
	#tokens[2] is the channel or recipient name.
	#tokens[3] is the full message with a leading colon. This needs to be stripped.
	if (len(tokens) > 1):
		#print(tokens)
		if (tokens[1] == "PRIVMSG"):
			if (len(tokens) > 2):
				if (tokens[3] == "\x01VERSION" or tokens[3] == "\x01VERSION\x01"):
					if (parent.guiParent != None):
						parent.guiParent.print("Received VERSION request from %s." % tokens[0], user = tokens[0])
						parent.guiParent.addUser(tokens[0], tokens[2])
						if (not parent.guiParent.isPluginInitialized):
							parent.guiParent.entryMessage = "/i"
							parent.guiParent.entryCommand("-1")
							parent.guiParent.isPluginInitialized = True
					parent.s.send(PRIVMSG(tokens[0], "WedrBot v1.0.X - Under Active Development", 1))
					parent.s.send(PRIVMSG(tokens[0], "Creator: wedr, Master of WedrBot", 1))
					parent.s.send(PRIVMSG(tokens[0], "Special Thanks: Tobago, Shadowhand, MasterCheese, Miah_Molkot, Zhenn, BogomilP, leo60228, Ghost37486,", 1))
					parent.s.send(PRIVMSG(tokens[0], "                flagrama, imanoob, Gelex, icecream, king_iix, Plailect, Redy, TricksterGuy, Ennea, Rubik", 1))
				elif (tokens[3] == "\x01ACTION" or tokens[3] == "\x01ACTION\x01"):
					if (parent.guiParent != None):
						parent.guiParent.print("[%s] * %s %s" % (tokens[2], tokens[0], getMessage(tokens, 4)), user = tokens[0])
						parent.guiParent.addUser(tokens[0], tokens[2])
					else:
						print("[%s] * %s %s" % (tokens[2], tokens[0], getMessage(tokens, 4)))
				else:
					caller = tokens[0]
					recipient = tokens[2]
					message = getMessage(tokens, 3)
					if (parent.guiParent != None):
						parent.guiParent.print(text = "[%s] <%s> %s" % (recipient, caller, message), user = caller)
						parent.guiParent.addUser(tokens[0], tokens[2])
						parent.guiParent.textOutput.see(tkinter.END)
					else:
						print("[%s] <%s> %s" % (recipient, caller, message))
		elif (tokens[1] == "NOTICE"):
			caller = tokens[0]
			recipient = tokens[2]
			message = getMessage(tokens, 3)
			if (parent.guiParent != None):
				parent.guiParent.print(text = "[NOTICE] -%s-: %s" % (caller, message), user = caller)
				parent.guiParent.textOutput.see(tkinter.END)
			else:
				print("[NOTICE] -%s-: %s" % (caller, message))

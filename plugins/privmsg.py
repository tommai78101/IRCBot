import codecs
import tkinter

from PluginBot import BYTE
from PluginBot import PRIVMSG
from PluginBot import getUser
from PluginBot import getMessage


class VersionCheck:
	flag = False
versionCheck = VersionCheck()

def version():
	codecs.register(lambda name: codecs.lookup("utf-8") if name == "cp65001" else None)
	versionCheck = False
	return "PrivMsg - v1.0"

def plugin_main(parent, tokens):
	#PRIVMSG protocol
	#tokens[0] gets the full user account. This needs to be stripped and splitted out.
	#tokens[1] is the command. PRIVMSG is a command.
	#tokens[2] is the channel or recipient name.
	#tokens[3] is the full message with a leading colon. This needs to be stripped.
	if (len(tokens) > 1):
		if (tokens[1] == "PRIVMSG"):
			if (len(tokens) > 2 and tokens[3] == "\x01VERSION\x01"):
				parent.s.send(PRIVMSG(tokens[0], "\x01VERSION WedrBot v1.0\x01", 1))
				if (parent.guiParent != None and not versionCheck.flag):
					parent.guiParent.entryMessage = "/i"
					parent.guiParent.entryCommand("-1")
					versionCheck.flag = True
			else:
				caller = tokens[0]
				recipient = tokens[2]
				message = getMessage(tokens, 3)
				if (parent.guiParent != None):
					parent.guiParent.print(text = "[%s] <%s> %s" % (recipient, caller, message))
					parent.guiParent.textOutput.see(tkinter.END)
				else:
					print("[%s] <%s> %s" % (recipient, caller, message))
		elif (tokens[1] == "NOTICE"):
			caller = tokens[0]
			recipient = tokens[2]
			message = getMessage(tokens, 3)
			if (parent.guiParent != None):
				parent.guiParent.print(text = "[NOTICE] -%s-: %s" % (caller, message))
				parent.guiParent.textOutput.see(tkinter.END)
			else:
				print("[NOTICE] -%s-: %s" % (caller, message))

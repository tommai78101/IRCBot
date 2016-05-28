import codecs

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
	if (len(tokens) > 1 and tokens[1] == "PRIVMSG"):
		if (len(tokens) > 2 and tokens[3] == ":\x01VERSION\x01"):
			print("Sending VERSION")
			parent.s.send(BYTE("NOTICE %s :\x01VERSION WedrBot v1.0\x01" % tokens[0]))
		else:
			caller = tokens[0]
			recipient = tokens[2]
			message = getMessage(tokens, 3)
			print("<%s> %s: %s" % (tokens[2], caller, message))

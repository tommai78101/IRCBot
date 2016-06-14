import codecs
from time import sleep
from PluginBot import BYTE

codecs.register(lambda name: codecs.lookup("utf-8") if name == "cp65001" else None)

def version():
	return "Kick - v1.0"

def plugin_main(parent, tokens):
	if (len(tokens) > 3):
		if (tokens[1] == "KICK" and tokens[3] == "WedrBot"):
			parent.leave(tokens[2], True)
			if (parent.guiParent != None):
				parent.guiParent.print("%s is kicked from channel, %s" % (tokens[3], tokens[2]))
				parent.guiParent.entryMessage = "/l %s" % tokens[2]
				parent.guiParent.entryCommand("-1")
			else:
				print("%s is kicked from channel, %s" % (tokens[3], tokens[2]))

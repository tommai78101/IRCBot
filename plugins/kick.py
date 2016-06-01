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
			print("WedrBot is kicked from channel, %s" % tokens[2])

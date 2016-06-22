from PluginBot import PRIVMSG

def version():
	return "Look of Disapproval v1.0"

def plugin_main(parent, tokens):
	if (len(tokens) > 3):
		if (tokens[3] == ".ugh" or tokens[3] == ".sigh" or tokens[3] == ".facepalm"):
			if (len(tokens) > 4):
				try:
					if (parent.guiParent != None):
						parent.guiParent.print(" -- %s ?_?" % tokens[4])
					else:
						print(" -- %s ?_?" % tokens[4])
				except:
					if (parent.guiParent != None):
						parent.guiParent.print("Giving the look of disapproval towards %s." % tokens[4])
					else:
						print("Giving the look of disapproval towards %s." % tokens[4])
			else:
				try:
					if (parent.guiParent != None):
						parent.guiParent.print("?_?")
					else:
						print("?_?")
				except:
					if (parent.guiParent != None):
						parent.guiParent.print("Giving the look of disapproval.")
					else:
						print("Giving the look of disapproval.")
				parent.s.send(PRIVMSG(tokens[2], "\u0ca0_\u0ca0", 0))
		elif (tokens[3] == ".help"):
			parent.s.send(PRIVMSG(tokens[0], "USAGE: .ugh / .sigh / .facepalm - Gives a look of disapproval.", 1))
			parent.s.send(PRIVMSG(tokens[0], "USAGE: .ugh / .sigh / .facepalm [user] - Gives a look of disapproval to the user.", 1))

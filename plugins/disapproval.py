from PluginBot import PRIVMSG

def version():
	return "Look of Disapproval v1.0"

def plugin_main(parent, tokens):
	if (len(tokens) > 3):
		if (tokens[3] == ".ugh" or tokens[3] == ".sigh" or tokens[3] == ".facepalm"):
			if (len(tokens) > 4):
				parent.s.send(PRIVMSG(tokens[2], " -- \u0ca0_\u0ca0 at %s." % tokens[4], 0))
				try:
					if (parent.guiParent != None):
						parent.guiParent.print(" -- %s ಠ_ಠ" % tokens[4])
					else:
						print(" -- %s ಠ_ಠ" % tokens[4])
				except:
					if (parent.guiParent != None):
						parent.guiParent.print("Giving the look of disapproval towards %s." % tokens[4])
					else:
						print("Giving the look of disapproval towards %s." % tokens[4])
			else:
				parent.s.send(PRIVMSG(tokens[2], " -- \u0ca0_\u0ca0", 0))
				try:
					if (parent.guiParent != None):
						parent.guiParent.print("\u0ca0_\u0ca0")
					else:
						print("ಠ_ಠ")
				except:
					if (parent.guiParent != None):
						parent.guiParent.print("Giving the look of disapproval.")
					else:
						print("Giving the look of disapproval.")
		elif (tokens[3] == ".flip"):
			parent.s.send(PRIVMSG(tokens[2], " -- (\u256f\u25e6\u25ab\u25e6)\u256f \u2312 \u2538\u2014\u2538", 0))
			#try:
			#	if (parent.guiParent != None):
			#		parent.guiParent.print(" (╯°□°)╯︵ ┻━┻")
			#	else:
			#		print(" (╯°□°)╯︵ ┻━┻")
			#except:
			#	if (parent.guiParent != None):
			#		parent.guiParent.print("Flips table!")
			#	else:
			#		print("Flips table!")
		elif (tokens[3] == ".help"):
			parent.s.send(PRIVMSG(tokens[0], "USAGE: .ugh / .sigh / .facepalm - Gives a look of disapproval.", 1))
			parent.s.send(PRIVMSG(tokens[0], "USAGE: .ugh / .sigh / .facepalm [user] - Gives a look of disapproval to the user.", 1))
			parent.s.send(PRIVMSG(tokens[0], "USAGE: .flip - Flips table.", 1))

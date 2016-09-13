from PluginBot import PRIVMSG
from PluginBot import getMessage

def version():
	return "Look of Disapproval v1.0"

def plugin_main(parent, tokens):
	if (len(tokens) > 3):
		if (tokens[3] == ".ugh" or tokens[3] == ".sigh"):
			if (len(tokens) > 4):
				parent.s.send(PRIVMSG(tokens[2], "  -- \u0ca0_\u0ca0 at %s." % tokens[4], 0))
				try:
					if (parent.guiParent != None):
						parent.guiParent.print("  -- %s ಠ_ಠ" % tokens[4])
					else:
						print("  -- %s ಠ_ಠ" % tokens[4])
				except:
					if (parent.guiParent != None):
						parent.guiParent.print("Giving the look of disapproval towards %s." % tokens[4])
					else:
						print("Giving the look of disapproval towards %s." % tokens[4])
			else:
				parent.s.send(PRIVMSG(tokens[2], "  -- \u0ca0_\u0ca0", 0))
				try:
					if (parent.guiParent != None):
						parent.guiParent.print("\u0ca0_\u0ca0")
					else:
						print("Giving the look of disapproval.")
				except:
					if (parent.guiParent != None):
						parent.guiParent.print("Giving the look of disapproval.")
					else:
						print("Giving the look of disapproval.")
		elif (tokens[3] == ".flip"):
			if (len(tokens) > 4):
				message = getMessage(tokens, 4)
				parent.s.send(PRIVMSG(tokens[2], "  -- (\u256f\u25e6\u25ab\u25e6)\u256f \u2312 \u2538\u2014\u2538   - %s" % message, 0))
				if (parent.guiParent != None):
					parent.guiParent.print("Flips table for %s!" % message)
				else:
					print("Flips table!")
			else:
				parent.s.send(PRIVMSG(tokens[2], "  -- (\u256f\u25e6\u25ab\u25e6)\u256f \u2312 \u2538\u2014\u2538", 0))
				if (parent.guiParent != None):
					parent.guiParent.print("Flips table!")
				else:
					print("Flips table!")
		elif (tokens[3] == ".cm" or tokens[3] == ".checkmate"):
			#☚(°ヮ°)☚ 
			if (len(tokens) > 4):
				message = getMessage(tokens, 4)
				parent.s.send(PRIVMSG(tokens[2], "  -- ☜(\u25e6\u30ee\u25e6)☜  - %s" % message, 0))
				if (parent.guiParent != None):
					parent.guiParent.print("Checkmate! ☜ with message")
				else:
					print("Checkmate! ☜ with message")
			else:
				parent.s.send(PRIVMSG(tokens[2], "  -- ☜(\u25e6\u30ee\u25e6)☜", 0))
				if (parent.guiParent != None):
					parent.guiParent.print("Checkmate! ☜ ")
				else:
					print("Checkmate! ☜ ")
		elif (tokens[3] == ".facepalm" or tokens[3] == ".fp"):
			if (len(tokens) > 4):
				parent.s.send(PRIVMSG(tokens[2], "  -- (-\u032d \u10da) at %s" % tokens[4], 0))
			else:
				parent.s.send(PRIVMSG(tokens[2], "  -- (-\u032d \u10da)", 0))
			if (parent.guiParent != None):
				parent.guiParent.print("Facepalm!")
			else:
				print("Facepalm!")
		elif (tokens[3] == ".le"):
			#´_>`
			if (len(tokens) > 4):
				message = getMessage(tokens, 4)
				parent.s.send(PRIVMSG(tokens[2], "  -- %s  ´_>`" % message, 0))
				if (parent.guiParent != None):
					parent.guiParent.print("´_>` with message")
				else:
					print("´_>` with message")
			else:
				parent.s.send(PRIVMSG(tokens[2], "  -- ´_>`", 0))
				if (parent.guiParent != None):
					parent.guiParent.print("´_>`")
				else:
					print("´_>`")
		elif (tokens[3] == ".wnk"):
			#(ง ͡~ ͜ʖ͡°)ᕤ ✧
			parent.s.send(PRIVMSG(tokens[2], "  -- \u0028\u00E07\u0020\u0361\u007E\u0020\u035C\u0296\u0361\u00B0\u0029\u1564\u0020\u2727", 0))
			try:
				if (parent.guiParent != None):
					parent.guiParent.print("\u0028\u00E07\u0020\u0361\u007E\u0020\u035C\u0296\u0361\u00B0\u0029\u1564\u0020\u2727")
				else:
					print("Giving the wink.")
			except:
				if (parent.guiParent != None):
					parent.guiParent.print("Giving the wink.")
				else:
					print("Giving the wink.")
		elif (tokens[3] == ".mf"):
			#ಠ︵ಠ 凸
			parent.s.send(PRIVMSG(tokens[2], "  -- \u0CA0\uFE35\u0CA0\u0020\u51F8", 0))
			try:
				if (parent.guiParent != None):
					parent.guiParent.print("\u0CA0\uFE35\u0CA0\u0020\u51F8")
				else:
					print("Giving the finger.")
			except:
				if (parent.guiParent != None):
					parent.guiParent.print("Giving the finger.")
				else:
					print("Giving the finger.")
		elif (tokens[3] == ".lenny"):
			#( ͡° ͜ʖ ͡° )
			parent.s.send(PRIVMSG(tokens[2], "  -- \u0028\u0020\u0361\u00B0\u0020\u035C\u0296\u0020\u0361\u00B0\u0020\u0029", 0))
			try:
				if (parent.guiParent != None):
					parent.guiParent.print("\u0028\u0020\u0361\u00B0\u0020\u035C\u0296\u0020\u0361\u00B0\u0020\u0029")
				else:
					print("Lenny.")
			except:
				if (parent.guiParent != None):
					parent.guiParent.print("Lenny.")
				else:
					print("Lenny.")
		elif (tokens[3] == ".help"):
			parent.s.send(PRIVMSG(tokens[0], "USAGE: .ugh / .sigh / .facepalm - Gives a look of disapproval.", 1))
			parent.s.send(PRIVMSG(tokens[0], "USAGE: .ugh / .sigh / .facepalm [user] - Gives a look of disapproval to the user.", 1))
			parent.s.send(PRIVMSG(tokens[0], "USAGE: .checkmate [message] / .cm [message] - Gives a sarcastic look with the optional following message.", 1))
			parent.s.send(PRIVMSG(tokens[0], "USAGE: .le [message] - Gives a sarcastic look with the optional following message.", 1))
			parent.s.send(PRIVMSG(tokens[0], "USAGE: .wnk - Gives a confident wink!", 1))
			parent.s.send(PRIVMSG(tokens[0], "USAGE: .mf - Gives THE FINGER.", 1))
			parent.s.send(PRIVMSG(tokens[0], "USAGE: .flip [message] - Flips table with the optional following message.", 1))

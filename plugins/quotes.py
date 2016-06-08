import os
import atexit
from PluginBot import BYTE
from PluginBot import PRIVMSG
from PluginBot import getUser
from PluginBot import getMessage

FILE_SEPARATOR = "\\"
quotesList = []
saveFileName = "quote"
tempFile = "quote.tmp"
saveFilePath = os.getcwd()

def createTempFile():
	file = open(saveFilePath + FILE_SEPARATOR + tempFile, "wb")
	file.write("".encode())

def openTempFile():
	return open(saveFilePath + FILE_SEPARATOR + tempFile, "ab")

def save():
	createTempFile()
	file = openTempFile()
	try:
		with file as f:
			for line in quotesList:
				f.write(line.encode())
	finally:
		if (file != None):
			file.close()
			file = None
	os.replace(saveFilePath + FILE_SEPARATOR + tempFile, saveFilePath + FILE_SEPARATOR + saveFileName)

def load():
	file = None
	try:
		file = open(saveFilePath + FILE_SEPARATOR + saveFileName, "rb")
		with file as f:
			quotesList.clear()
			f.seek(0)
			for line in file:
				temp = line.decode()
				if (temp != "\n"):
					quotesList.append(temp)
	except:
		if (file != None):
			file.close()
			file = None
	finally:
		if (file != None):
			file.close()
			file = None

def version():
	load()
	atexit.register(save)
	return "Quotes - v1.0"

def plugin_main(parent, tokens):
	message = getMessage(tokens)
	if (len(tokens) > 3):
		#Blocking channels.
		if (tokens[2] == "#3dshacks"):
			return
		if (tokens[3] == ".wedr"):
			if (len(tokens) > 4):
				if (tokens[4] == "add"):
					if (len(tokens) > 5):
						tempString = ""
						for i in range(5, len(tokens)):
							tempString += tokens[i] + " "
						quotesList.append("[%s] %s" % (tokens[0], tempString))
						print("Quote has been added.")
						parent.s.send(PRIVMSG(tokens[2], "Quote added.", 0))
					else:
						parent.s.send(PRIVMSG(tokens[2], "USAGE: .wedr add <MESSAGE> - Add MESSAGE to Quotes List.", 0))
				elif (tokens[4].isnumeric()):
					try:
						quoteIndex = int(tokens[4])
						if (quoteIndex > len(quotesList) or quoteIndex <= 0):
							print("Index is invalid.")
							parent.s.send(PRIVMSG(tokens[2], "Invalid quote index. Enter number from 1 to %d." % (len(quotesList)), 0))
						else:
							print("Showing quote #%s" % (str(quotesList[quoteIndex - 1])))
							parent.s.send(PRIVMSG(tokens[2], "Quote #%s: %s" % (str(quoteIndex), str(quotesList[quoteIndex - 1])), 0))
					except ValueError:
						print("Error converting string to integer.")
					except Exception as error:
						print("Error - %s" % (str(error)))
				elif (tokens[4] == "remove"):
					if (len(tokens) > 5 and tokens[5].isnumeric()):
						try:
							quoteIndex = int(tokens[5])
							if (quoteIndex > len(quotesList) or quoteIndex <= 0):
								print("Index is invalid.")
								parent.s.send(PRIVMSG(tokens[2], "Invalid quote index. Enter number from 1 to %d." % (len(quotesList)), 0))
							else:
								quotesList.remove(quotesList[quoteIndex - 1])
								print("Successfully removed quote #%s" % (tokens[5]))
								parent.s.send(PRIVMSG(tokens[2], "Quote #%s has been removed." % (tokens[5]), 0))
						except Exception:
							print("Quote #%s does not exist." % (tokens[5]))
							parent.s.send(PRIVMSG(tokens[2], "Quote #%s does not exist." % (tokens[5]), 0))
					else:
						if (len(quotesList) == 0):
							print("Quotes List empty.")
							parent.s.send(PRIVMSG(tokens[2], "USAGE: .wedr remove <INDEX> - Remove MESSAGE matching INDEX from Quotes List. Quotes List is currently empty.", 0))
						else:
							print("Index not given.")
							parent.s.send(PRIVMSG(tokens[2], "USAGE: .wedr remove <INDEX> - Remove MESSAGE matching INDEX (range: 1 to %d) from Quotes List." % (len(quotesList)), 0))
				elif (tokens[4] == "capacity" or tokens[4] == "size"):
					print("Showing quotes list size.")
					parent.s.send(PRIVMSG(tokens[2], "Quotes List size : %d" % (len(quotesList)), 0))
				elif (tokens[4] == "help"):
					parent.s.send(PRIVMSG(tokens[0], "USAGE: .wedr add <MESSAGE> - Add MESSAGE to Quotes List.", 1))
					parent.s.send(PRIVMSG(tokens[0], "USAGE: .wedr remove <INDEX> - Removes quote from Quotes List.", 1))
					parent.s.send(PRIVMSG(tokens[0], "USAGE: .wedr <INDEX> - Outputs quote from Quotes List.", 1))
					parent.s.send(PRIVMSG(tokens[0], "USAGE: .wedr size - Outputs quote list size from Quotes List.", 1))
					parent.s.send(PRIVMSG(tokens[0], "USAGE: .wedr capacity - Outputs quote list size from Quotes List.", 1))
					parent.s.send(PRIVMSG(tokens[0], "USAGE: .wedr help - Brings up all commands and descriptions.", 1))
				elif (tokens[4] == "save"):
					save()
					print("Quotes List saved.")
					parent.s.send(PRIVMSG(tokens[2], "Quotes List is saved.", 0))
				elif (tokens[4] == "load"):
					load()
					print("Quotes List loaded.")
					parent.s.send(PRIVMSG(tokens[2], "Quotes List is loaded.", 0))
			else:
				print("Incorrect usage detected.")
				parent.s.send(PRIVMSG(tokens[0], "USAGE: .wedr <Command> - Type \".wedr help\" for more info.", 1))
		elif (tokens[3] == ".help"):
			print("Requiring help detected.")
			parent.s.send(PRIVMSG(tokens[0], "USAGE: .wedr <Command> - Type \".wedr help\" for more info.", 1))
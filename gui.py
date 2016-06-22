import random
import threading
import tkinter
import tkinter.scrolledtext
import collections
import re

from operator import attrgetter
from time import sleep

from PluginBot import PluginBot
from PluginBot import BYTE

def rgb(red, green, blue):
	return "#%02x%02x%02x" % (red, green, blue)

class GUI:
	root = None
	textOutput = None
	entryMessage = ""
	bot = None
	entry = None
	channelTags = dict()
	isPluginInitialized = False
	usernameList = dict()
	lastUserSuggestion = ""

	def __init__(self):
		self.root = tkinter.Tk()
		self.root.title("WedrBot - IRC Bot Client")

		width = 650
		height = 500
		self.root.minsize(width, height)

		logMessageFrame = tkinter.Frame(master = self.root)
		logMessageFrame.grid(row = 0, column = 0, sticky = (tkinter.N, tkinter.W, tkinter.E, tkinter.S))
		self.textOutput = tkinter.scrolledtext.ScrolledText(master = logMessageFrame, wrap = tkinter.WORD)
		self.textOutput.config(state = tkinter.DISABLED)
		self.textOutput.pack(expand = 1, fill = tkinter.BOTH)

		userInputFrame = tkinter.Frame(master = self.root, borderwidth = 4)
		userInputFrame.grid(row = 1, column = 0, sticky = (tkinter.W, tkinter.E, tkinter.S), pady = 2)
		#button = tkinter.Button(master = userInputFrame, text = "Send", command = lambda: self.sendMessage(None))
		#button.bind("<Return>", self.sendMessage)
		#button.grid(row = 0, column = 0, sticky = (tkinter.W, tkinter.E), padx = 1.5)
		self.entry = tkinter.Entry(master = userInputFrame)
		self.entry.bind("<Return>", self.entryCommand)
		self.entry.bind("<Tab>", lambda event: self.autocomplete(event, self.entry.get()))
		self.entry.grid(row = 0, column = 0, sticky = (tkinter.W, tkinter.E), padx = 1.5)

		self.root.grid_rowconfigure(0, weight = 15)
		self.root.grid_rowconfigure(1, weight = 1)
		self.root.grid_columnconfigure(0, weight = 1)
		userInputFrame.grid_rowconfigure(0, weight = 1)
		userInputFrame.grid_columnconfigure(0, weight = 1)
		#userInputFrame.grid_columnconfigure(1, weight = 7)

		self.bot = PluginBot(self)
		self.bot.connect()
		self.bot.start()

		self.addChannel(self.bot.focusedChannel)
		sortedDict = sorted(self.channelTags, key = lambda x: x.length)
		for i in range(0, len(sortedDict)):
			self.textOutput.tag_configure(self.bot.focusedChannel, foreground = self.channelTags[sortedDict[i - len(sortedDict)]])
		self.textOutput.tag_configure("red", foreground = rgb(255, 0, 0))

	def run(self):
		self.root.mainloop()

	def print(self, text = "", user = None):
		if (text != ""):
			self.textOutput.config(state = "normal")
			self.textOutput.insert(tkinter.END, "\n%s" % text)
			try:
				indexCount = int(self.textOutput.index("%s-1c" % tkinter.END).split(".")[0])
				if (indexCount > 300):
					#Index number count starts from 1.0.
					# X.Y:  X is the line number. Y is the character index of line X.
					self.textOutput.delete("1.0", "2.0")
			except Exception as err:
				self.print(err)
			sortedDict = sorted(self.channelTags, key = attrgetter("length"))
			if (len(sortedDict) > 0):
				for i in range(0, len(sortedDict)):
					self.tagPattern(sortedDict[i-len(sortedDict)].name, sortedDict[i - len(sortedDict)].name)
			if (self.bot != None):
				self.tagUserPattern(self.bot.nickName, "red", user)
			self.textOutput.see(tkinter.END)
			self.textOutput.config(state = tkinter.DISABLED)

	def sendMessage(self, event):
		if (self.entryMessage != ""):
			if (self.bot.focusedChannel == ""):
				self.print("You are not in any channel.")
			else:
				tempString = "[%s] <%s> %s" % (self.bot.focusedChannel, self.bot.nickName, self.entryMessage)
				if (self.entryMessage[0] == "."):
					self.bot.s.send(BYTE("PRIVMSG %s :%s" % (self.bot.focusedChannel, self.entryMessage)))
					tokenString = "%s PRIVMSG %s :%s" % (self.bot.nickName, self.bot.focusedChannel, self.entryMessage)
					self.bot.handleTokens(self.bot.makeTokens(tokenString))
				else:
					self.bot.s.send(BYTE("PRIVMSG %s :%s" % (self.bot.focusedChannel, self.entryMessage)))
					self.print(text = tempString)
				self.textOutput.see(tkinter.END)
				self.entry.delete(0, tkinter.END)

	def randomColor(self):
		randomTextColor = "#%02x%02x%02x" % (random.randint(90, 200), random.randint(90, 200), random.randint(90, 200))
		return randomTextColor

	def getUserInput(self, event):
		if (event != "-1"):
			self.entryMessage = self.entry.get()
			self.entry.delete(0, tkinter.END)

	def addChannel(self, channel):
		Channel = collections.namedtuple("Channel", ["name", "length"])
		c = Channel(name = channel, length = len(channel))
		if (c not in self.channelTags):
			self.channelTags[c] = self.randomColor()
		return sorted(self.channelTags, key = lambda x: x.length)

	def addUser(self, user, channel):
		if (channel not in self.usernameList):
			self.usernameList.setdefault(channel, [])
		if (user not in self.usernameList[channel]):
			self.usernameList[channel].append(user)

	def tagPattern(self, pattern, tag):
		start = "1.0"
		end = tkinter.END
		self.textOutput.mark_set("matchStart", start)
		self.textOutput.mark_set("matchEnd", start)
		self.textOutput.mark_set("searchLimit", end)
		count = tkinter.IntVar()
		legitSymbols = [".", ",", " ", "!", "]", "\n", "\r", ")", "&", "?", "=", "'", '"', ";"]
		while True:
			index = self.textOutput.search(pattern, "matchEnd", "searchLimit", count = count, regexp = False)
			if (index == "" or count.get() == 0):
				break;
			check = False
			try:
				newIndex = "%s+%dc" % (index, count.get())
				temp = self.textOutput.get(newIndex, "%s+1c" % newIndex)
				if (temp not in legitSymbols):
					check = True
			except:
				check = True
			
			if (not check):
				self.textOutput.mark_set("matchStart", index)
				self.textOutput.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
				self.textOutput.tag_add(tag, "matchStart", "matchEnd")
			else:
				self.textOutput.mark_set("matchEnd", "%s+%sc" % (index, count.get()+1))

	def tagUserPattern(self, pattern, tag, user):
		start = "1.0"
		end = tkinter.END
		self.textOutput.mark_set("matchStart", start)
		self.textOutput.mark_set("matchEnd", start)
		self.textOutput.mark_set("searchLimit", end)
		count = tkinter.IntVar()
		newIndexOffset = 1
		while True:
			reg = r"(%s([^\>\]]|\,|\.|\ |\:))" % pattern
			index = self.textOutput.search(reg, "matchEnd", "searchLimit", count = count, regexp = True)
			if (index == "" or count.get() == 0):
				break;
			lineIndex = "%s.0" % index.split(".")[0]
			otherCount = tkinter.IntVar()
			reg = r"\*\ [A-Za-z]+\ " if user == None else r"\*\ %s\ " % user
			newIndex = self.textOutput.search(reg, lineIndex, "%s lineend" % lineIndex, count = otherCount, regexp = True)
			if (newIndex == "" or otherCount.get() == 0):
				reg = r"\<.+\>" if user == None else r"\<%s\>" % user
				newIndex = self.textOutput.search(reg, lineIndex, "%s lineend" % lineIndex, count = otherCount, regexp = True)
				if (newIndex == "" or otherCount.get() == 0):
					self.textOutput.mark_set("matchEnd", "%s+1l" % lineIndex)
					continue;
				else:
					newIndexOffset = 1
			else:
				newIndexOffset = 2
			newIndex = "%s.%s" % (newIndex.split(".")[0], int(newIndex.split(".")[1]) + newIndexOffset)
			self.textOutput.mark_set("matchStart", newIndex)
			self.textOutput.mark_set("matchEnd", "%s+%sc" % (newIndex, otherCount.get()-2))
			self.textOutput.tag_add(tag, "matchStart", "matchEnd")
			self.textOutput.mark_set("matchEnd", "%s+1l" % lineIndex)

	def rejoin(self, event):
		#Only used for initializing the bot. Do not use unless explicitly required.
		sortedDict = sorted(self.channelTags, key = lambda x: x.length)
		for i in range(0, len(sortedDict)):
			#self.entryMessage = ("/l %s" % sortedDict[i - len(sortedDict)].name)
			#self.entryCommand("-1")
			self.entryMessage = ("/j %s" % sortedDict[i - len(sortedDict)].name)
			self.entryCommand("-1")

		sleep(0.5)
		self.entryMessage = "/c"
		self.entryCommand("-1")
		self.entryMessage = "/u clear"
		self.entryCommand("-1")
		self.print("  --  Welcome to Channel %s. Type /help for more info.      --" % self.bot.focusedChannel)
		self.print("  --  Type in the input text area, then press ENTER key to chat.  --")
		self.print(" ")
		return

	def autocomplete(self, event, token, lower = True):
		cursorIndex = self.entry.index(tkinter.INSERT)
		cursorIndexBegin = cursorIndex-1
		cursorIndexEnd = cursorIndex+1
		try:
			if (token[cursorIndexBegin] == " "):
				cursorIndexBegin -= 1
			while (token[cursorIndexBegin] != " "):
				cursorIndexBegin -= 1
		except:
			cursorIndexBegin = 0
		try:
			if (token[cursorIndexEnd] == " "):
				cursorIndexEnd += 1
			while (token[cursorIndexEnd] != " "):
				cursorIndexEnd += 1
		except:
			cursorIndexEnd = self.entry.index(tkinter.END)
		if (cursorIndexBegin < 0):
			cursorIndexBegin = 0
		tempToken = token[cursorIndexBegin:cursorIndexEnd].strip(" ")
		try:
			if (self.lastUserSuggestion != tempToken):
				tempDict = dict()
				for user in self.usernameList[self.bot.focusedChannel]:
					for i in range(0, len(tempToken)):
						if (lower):
							if (tempToken[i].lower() == user[i].lower()):
								tempDict[user] = i
							else:
								break;
						else:
							if (tempToken[i].upper() == user[i].upper()):
								tempDict[user] = i
							else:
								break;
				sortedDict = sorted(tempDict, key = lambda x: x[1])
				if (len(sortedDict) > 0):
					self.lastUserSuggestion = sortedDict[0]
					self.entry.delete(cursorIndexBegin, tkinter.END)
					self.entry.insert(cursorIndexBegin, "%s " % self.lastUserSuggestion if cursorIndexBegin == 0 else " %s" % self.lastUserSuggestion)
				elif (lower == True):
					self.autocomplete(event, token, lower = False)
			else:
				tempList = self.usernameList[self.bot.focusedChannel]
				self.lastUserSuggestion = tempList[(tempList.index(tempToken) + 1) % len(tempList)]
				self.entry.delete(cursorIndexBegin, tkinter.END)
				self.entry.insert(cursorIndexBegin, "%s " % self.lastUserSuggestion if cursorIndexBegin == 0 else " %s" % self.lastUserSuggestion)
			#We return the string, "break", for tcl/tkinter to drop double events, due to TAB key firing off multiple platform-specific events.
			return "break"
		except:
			#We return the string, "break", for tcl/tkinter to drop double events, due to TAB key firing off multiple platform-specific events.
			return "break"

	def showUserList(self, channel):
		try:
			arrayList = self.usernameList[channel]
		except:
			self.usernameList.setdefault(channel, [])
			arrayList = self.usernameList[channel]
		if (len(arrayList) <= 0):
			self.print("Known users list in %s is empty." % channel)
			return;
		tempStr = ""
		for i in range(0, len(arrayList)):
			if (i != len(arrayList) - 1):
				tempStr += "%s, " % arrayList[i]
			else:
				tempStr += "%s" % arrayList[i]
		self.print("Known %s users list: %s" % (channel, tempStr))

	def entryCommand(self, event):
		#Handles all user inputs
		#If event is str(-1), then it skips obtaining user input.
		self.getUserInput(event)
		if (self.entryMessage != ""):
			tokens = self.entryMessage.split(" ")
			if (tokens[0] == "/j" or tokens[0] == "/join"):
				#Joining channels
				if (len(tokens) > 2):
					for i in range(1, len(tokens)):
						if (tokens[i][0] != "#"):
							tokens[i] = "#%s" % tokens[i]
						if (tokens[i] not in self.channelTags):
							self.addChannel(tokens[i])
							for j in range(0, len(sortedDict)):
								if (tokens[1] == sortedDict[j].name):
									self.textOutput.tag_configure(tokens[1], foreground = self.channelTags[sortedDict[j]])
									break
						self.bot.switch(tokens[i])
				elif (len(tokens) == 2):
					if (tokens[1][0] != "#"):
						tokens[1] = "#%s" % tokens[1]
					if (tokens[1] not in self.channelTags):
						sortedDict = self.addChannel(tokens[1])
						for i in range(0, len(sortedDict)):
							if (tokens[1] == sortedDict[i].name):
								self.textOutput.tag_configure(tokens[1], foreground = self.channelTags[sortedDict[i]])
								break
					self.bot.switch(tokens[1])
				else:
					self.print("Incorrect usage:  /join [channel]")
				self.entry.delete(0, tkinter.END)
			elif (tokens[0] == "/q" or tokens[0] == "/e" or tokens[0] == "/quit" or tokens[0] == "/exit"):
				#Quitting the bot client. Make sure to press any keys in the terminal/command prompt after use.
				print("Quitting bot.")
				self.bot.quit()
				self.bot.join()
				print("Quitting tkinter GUI.")
				self.root.destroy()
				return
			elif (tokens[0] == "/i" or tokens[0] == "/identify"):
				#Identifying the bot to the IRC host, only when the bot is unable to request for verbose, but the connection is still valid.
				self.bot.identify();
				workerThread = threading.Thread(target = self.rejoin, args = (event,))
				workerThread.start()
			elif (tokens[0] == "/c" or tokens[0] == "/clear"):
				#Clearing the text output screen.
				self.textOutput.config(state = "normal")
				if (len(tokens) > 1 and tokens[1] == "tag"):
					sortedDict = sorted(self.channelTags, key = lambda x: x.length)
					for i in range(0, len(sortedDict)):
						self.textOutput.tag_delete(sortedDict[i].name)
				self.textOutput.delete("1.0", tkinter.END)
				self.textOutput.config(state = tkinter.DISABLED)
			elif (tokens[0] == "/r" or tokens[0] == "/reload"):
				#Reloading plugins.
				self.bot.reloadAll()
			elif (tokens[0] == "/f" or tokens[0] == "/focus"):
				self.print("Focused channel is %s." % self.bot.focusedChannel)
			elif (tokens[0] == "/u" or tokens[0] == "/userlist" or tokens[0] == "/userslist"):
				if (len(tokens) > 1):
					if (tokens[1] == "clear"):
						self.usernameList.clear()
					else:
						if (tokens[1][0] != "#"):
							tokens[1] = "#%s" % tokens[1]
						self.showUserList(tokens[1])
				else:
					self.showUserList(self.bot.focusedChannel)
			elif (tokens[0] == "/l" or tokens[0] == "/leave"):
				#Leaving channels
				sortedDict = sorted(self.channelTags, key = lambda x: x.length)
				if (len(tokens) > 2):
					for i in range(1, len(tokens)):
						if (tokens[i][0] != "#"):
							tokens[i] = "#%s" % tokens[i]
						check = False
						for j in range(0, len(sortedDict)):
							if (sortedDict[j].name == tokens[i]):
								self.channelTags.pop(sortedDict[j])
								check = True
						if (check):
							self.bot.leave(tokens[i], True)
							self.textOutput.tag_delete(tokens[i])
							if (len(self.channelTags) > 0):
								sortedDict = sorted(self.channelTags, key = lambda x: x.length)
								self.bot.switch(sortedDict[len(self.channelTags)-1].name)
							else:
								self.bot.switch("", False)
						else:
							self.print("Channel, %s, is not on the channel list." % tokens[i])
				elif (len(tokens) == 2):
					if (tokens[1][0] != "#"):
						tokens[1] = "#%s" % tokens[1]
					check = False
					for i in range(0, len(sortedDict)):
						if (sortedDict[i].name == tokens[1]):
							self.channelTags.pop(sortedDict[i])
							check = True
					if (check):
						self.bot.leave(tokens[1], True)
						self.textOutput.tag_delete(tokens[1])
						if (len(self.channelTags) > 0):
							sortedDict = sorted(self.channelTags, key = lambda x: x.length)
							self.bot.switch(sortedDict[len(self.channelTags)-1].name)
						else:
							self.bot.switch("", False)
					else:
						self.print("Channel, %s, is not on the channel list." % tokens[1])
				else:
					self.print("Incorrect usage:  /leave [channel]")
				self.entry.delete(0, tkinter.END)
			elif (tokens[0] == "/a" or tokens[0] == "/active"):
				#Gives a list of all channels the bot is active in, or has joined in.
				tempList = ""
				sortedDict = sorted(self.channelTags, key = lambda x: x.name)
				if (len(sortedDict) <= 0):
					self.print("Joined Channel List is empty.")
				else:
					for i in range(0, len(sortedDict)):
						tempName = sortedDict[i].name
						if (tempName == self.bot.focusedChannel):
							tempName = "[[%s]]" % tempName
						tempList += tempName
						if (i < len(sortedDict)-1):
							tempList += ", "
					self.print("Joined Channel List: %s" % tempList)
			elif (tokens[0] == "/?" or tokens[0] == "/help"):
				#Help command.
				self.print(" ")
				self.print("Type anything in the input text area, then press ENTER key to chat with others.")
				self.print(" 1. /? or /help -- Bring up the bot commands.")
				self.print(" 2. /a or /active -- Shows the joined channel list.")
				self.print(" 3. /c or /clear -- Clear the text output screen.")
				self.print(" 4. /e or /exit -- Quit the bot.")
				self.print(" 5. /f or /focus -- Print currently focused channel.")
				self.print(" 6. /j or /join -- Join a new channel. Channel focus will switch over.")
				self.print(" 7. /l or /leave -- Leave channel. Channel focus will change.")
				self.print(" 8. /q or /quit -- Quit the bot.")
				self.print(" 9. /r or /reload -- Reload all plugins. (Hotswapping is supported.)")
				self.print("10. /u or /userlist -- Shows the users list.")
				if (self.bot.focusedChannel == ""):
					self.print(" ")
					self.print("You are currently not joined in any channel.")
			else:
				#Send commands over.
				self.sendMessage(event)



import random
import threading
import tkinter
import tkinter.scrolledtext
import collections

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

	def __init__(self):
		self.root = tkinter.Tk()
		self.root.title("WedrBot - IRC Bot Client")

		width = 650
		height = 500
		self.root.minsize(width, height)

		logMessageFrame = tkinter.Frame(master = self.root)
		logMessageFrame.grid(row = 0, column = 0, sticky = (tkinter.N, tkinter.W, tkinter.E, tkinter.S))
		self.textOutput = tkinter.scrolledtext.ScrolledText(master = logMessageFrame, wrap = tkinter.WORD)
		self.textOutput.pack(expand = 1, fill = tkinter.BOTH)

		userInputFrame = tkinter.Frame(master = self.root, borderwidth = 4)
		userInputFrame.grid(row = 1, column = 0, sticky = (tkinter.W, tkinter.E, tkinter.S), pady = 2)
		button = tkinter.Button(master = userInputFrame, text = "Send", command = lambda: self.sendMessage(None))
		button.bind("<Return>", self.sendMessage)
		button.grid(row = 0, column = 0, sticky = (tkinter.W, tkinter.E), padx = 1.5)
		self.entry = tkinter.Entry(master = userInputFrame)
		self.entry.bind("<Return>", self.entryCommand)
		self.entry.grid(row = 0, column = 1, sticky = (tkinter.W, tkinter.E), padx = 1.5)

		self.root.grid_rowconfigure(0, weight = 15)
		self.root.grid_rowconfigure(1, weight = 1)
		self.root.grid_columnconfigure(0, weight = 1)
		userInputFrame.grid_rowconfigure(0, weight = 1)
		userInputFrame.grid_columnconfigure(0, weight = 1)
		userInputFrame.grid_columnconfigure(1, weight = 7)

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

	def print(self, text = ""):
		if (text != ""):
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
			for i in range(0, len(sortedDict)):
				self.tagPattern(sortedDict[i-len(sortedDict)].name, sortedDict[i - len(sortedDict)].name)
			if (self.bot != None):
				self.tagUserPattern(self.bot.nickName, "red")
			self.textOutput.see(tkinter.END)


	def sendMessage(self, event):
		if (self.entryMessage != ""):
			tempString = "[%s] <%s> %s" % (self.bot.focusedChannel, self.bot.nickName, self.entryMessage)
			if (self.entryMessage[0] == "."):
				self.bot.s.send(BYTE("PRIVMSG %s :%s" % (self.bot.focusedChannel, self.entryMessage)))
				tokenString = "%s PRIVMSG %s :%s" % (self.bot.nickName, self.bot.focusedChannel, self.entryMessage)
				self.bot.handleTokens(self.bot.makeTokens(tokenString))
			else:
				self.bot.s.send(BYTE("PRIVMSG %s :%s" % (self.bot.focusedChannel, self.entryMessage)))
				self.print(text = tempString)
			self.textOutput.see(tkinter.END)
			#self.entryMessage = ""
			self.entry.delete(0, tkinter.END)

	def randomColor(self):
		randomTextColor = "#%02x%02x%02x" % (random.randint(50, 225), random.randint(50, 225), random.randint(50, 225))
		return randomTextColor

	def getUserInput(self, event):
		if (event != "-1"):
			self.entryMessage = self.entry.get()
			self.entry.delete(0, tkinter.END)

	def addChannel(self, channel):
		Channel = collections.namedtuple("Channel", ["name", "length"])
		c = Channel(name = channel, length = len(channel))
		self.channelTags[c] = self.randomColor()
		return sorted(self.channelTags, key = lambda x: x.length)

	def tagPattern(self, pattern, tag):
		start = "1.0"
		end = tkinter.END
		self.textOutput.mark_set("matchStart", start)
		self.textOutput.mark_set("matchEnd", start)
		self.textOutput.mark_set("searchLimit", end)
		count = tkinter.IntVar()
		while True:
			reg = r"(%s([^\>]|\,|\.|\ |\:))" % pattern
			index = self.textOutput.search(reg, "matchEnd", "searchLimit", count = count, regexp = True)
			if (index == "" or count.get() == 0):
				break;
			self.textOutput.mark_set("matchStart", index)
			self.textOutput.mark_set("matchEnd", "%s+%sc" % (index, count.get()-1))
			check = False

			temp = self.textOutput.get(index, "%s+%sc" % (index, count.get()))
			try:
				o = ord(temp[len(temp)-1])
				if (o < ord("0") or (ord("9") < o and o < ord("A")) or (ord("Z") < o and o < ord("a")) or (ord("z") < o)):
					check = False
				else:
					check = True
			except:
				check = True
			
			tags = self.textOutput.tag_names(index)
			try:
				for i in range(0, len(tags)):
					if (tags[i] == tag):
						check = True
					if (tags[i] in pattern):
						check = True
					if (pattern in tags[i]):
						check = True
				if (not check):
					self.textOutput.tag_add(tag, "matchStart", "matchEnd")
			except:
				continue

	def tagUserPattern(self, pattern, tag):
		start = "1.0"
		end = tkinter.END
		self.textOutput.mark_set("matchStart", start)
		self.textOutput.mark_set("matchEnd", start)
		self.textOutput.mark_set("searchLimit", end)
		count = tkinter.IntVar()
		while True:
			reg = r"(%s([^\>\]]|\,|\.|\ |\:))" % pattern
			index = self.textOutput.search(reg, "matchEnd", "searchLimit", count = count, regexp = True)
			if (index == "" or count.get() == 0):
				break;
			lineIndex = "%s.0" % index.split(".")[0]
			otherCount = tkinter.IntVar()
			reg = r"\<.+\>"
			newIndex = self.textOutput.search(reg, lineIndex, "%s lineend" % lineIndex, count = otherCount, regexp = True)
			if (index == "" or otherCount.get() == 0):
				self.textOutput.mark_set("matchEnd", "%s+1l" % lineIndex)
				continue;
			newIndex = "%s.%s" % (newIndex.split(".")[0], int(newIndex.split(".")[1]) + 1)
			self.textOutput.mark_set("matchStart", newIndex)
			self.textOutput.mark_set("matchEnd", "%s+%sc" % (newIndex, otherCount.get()-1))
			self.textOutput.tag_add(tag, "matchStart", "matchEnd")
			self.textOutput.mark_set("matchEnd", "%s+1l" % lineIndex)

	def rejoin(self, event):
		sortedDict = sorted(self.channelTags, key = lambda x: x.length)
		for i in range(0, len(sortedDict)):
			self.entryMessage = ("/l %s" % sortedDict[i - len(sortedDict)].name)
			self.entryCommand("-1")
			self.entryMessage = ("/j %s" % sortedDict[i - len(sortedDict)].name)
			self.entryCommand("-1")
		self.entryMessage = "/c"
		self.entryCommand("-1")
		self.print("  --  Welcome to the channel, %s. Type /help for more info.  --" % self.bot.focusedChannel)
		self.print(" ")
		return

	def entryCommand(self, event):
		self.getUserInput(event)
		if (self.entryMessage != ""):
			tokens = self.entryMessage.split(" ")
			if (tokens[0] == "/j" or tokens[0] == "/join"):
				#Joining channels
				if (len(tokens) > 2):
					for i in range(1, len(tokens)):
						if (tokens[i][0] != "#"):
							tokens[i] = "#%s" % tokens[i]
						self.bot.switch(tokens[i])
						self.print("Joining channel %s" % tokens[i])
						if (tokens[i] not in self.channelTags):
							self.addChannel(tokens[i])
							for j in range(0, len(sortedDict)):
								if (tokens[1] == sortedDict[j].name):
									self.textOutput.tag_configure(tokens[1], foreground = self.channelTags[sortedDict[j]])
									break
				elif (len(tokens) == 2):
					if (tokens[1][0] != "#"):
						tokens[1] = "#%s" % tokens[1]
					self.bot.switch(tokens[1])
					self.print("Joining channel %s" % tokens[1])
					if (tokens[1] not in self.channelTags):
						sortedDict = self.addChannel(tokens[1])
						for i in range(0, len(sortedDict)):
							if (tokens[1] == sortedDict[i].name):
								self.textOutput.tag_configure(tokens[1], foreground = self.channelTags[sortedDict[i]])
								break
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
				if (len(tokens) > 1 and tokens[1] == "tag"):
					sortedDict = sorted(self.channelTags, key = lambda x: x.length)
					for i in range(0, len(sortedDict)):
						self.textOutput.tag_delete(sortedDict[i].name)
				self.textOutput.delete("1.0", tkinter.END)
			elif (tokens[0] == "/r" or tokens[0] == "/reload"):
				#Reloading plugins.
				self.bot.reloadAll()
			elif (tokens[0] == "/l" or tokens[0] == "/leave"):
				#Leaving channels
				sortedDict = sorted(self.channelTags, key = lambda x: x.length)
				if (len(tokens) > 2):
					for i in range(1, len(tokens)):
						if (tokens[i][0] != "#"):
							tokens[i] = "#%s" % tokens[i]
						self.bot.leave(tokens[i], True)
						self.print("Leaving channel %s" % tokens[i])
						for j in range(0, len(sortedDict)):
							if (sortedDict[j].name == tokens[i]):
								self.channelTags.pop(sortedDict[j])
								break
						self.textOutput.tag_delete(tokens[i])
				elif (len(tokens) == 2):
					if (tokens[1][0] != "#"):
						tokens[1] = "#%s" % tokens[1]
					self.bot.leave(tokens[1], True)
					self.print("Leaving channel %s" % tokens[1])
					for i in range(0, len(sortedDict)):
						if (sortedDict[i].name == tokens[1]):
							self.channelTags.pop(sortedDict[i])
							break
					self.textOutput.tag_delete(tokens[1])
				else:
					self.print("Incorrect usage:  /leave [channel]")
				self.entry.delete(0, tkinter.END)
			elif (tokens[0] == "/help" or tokens[0] == "/?"):
				#Help command.
				self.print("1. Type anything to chat with others in %s." % self.bot.focusedChannel)
				self.print("2. /? or /help -- Bring up the bot commands.")
				self.print("3. /j or /join -- Join a new channel. Channel focus will switch over.")
				self.print("4. /l or /leave -- Leave channel. Channel focus will change.")
				self.print("5. /c or /clear -- Clear the text output screen.")
				self.print("6. /r or /reload -- Reload all plugins. (Hotswapping is supported.)")
				self.print("7. /q or /quit -- Quit the bot.")
			else:
				#Send commands over.
				self.sendMessage(event)



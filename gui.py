import tkinter
import tkinter.scrolledtext

from time import sleep

from PluginBot import PluginBot
from PluginBot import BYTE


class GUI:
	root = None
	textOutput = None
	entryMessage = ""
	bot = None
	entry = None

	def __init__(self):
		self.root = tkinter.Tk()

		width = 450
		height = 150
		self.root.minsize(width, height)

		logMessageFrame = tkinter.Frame(master = self.root)
		logMessageFrame.grid(row = 0, column = 0, sticky = (tkinter.N, tkinter.W, tkinter.E))
		self.textOutput = tkinter.scrolledtext.ScrolledText(master = logMessageFrame, wrap = tkinter.WORD)
		self.textOutput.pack(expand = True)

		userInputFrame = tkinter.Frame(master = self.root, borderwidth = 5)
		userInputFrame.grid(row = 1, column = 0, sticky = (tkinter.W, tkinter.E, tkinter.S))
		button = tkinter.Button(master = userInputFrame, text = "Send", command = lambda: self.sendMessage(None))
		button.bind("<Return>", self.sendMessage)
		button.grid(row = 0, column = 0, sticky = (tkinter.W, tkinter.E), padx = 1.5)
		self.entry = tkinter.Entry(master = userInputFrame)
		self.entry.bind("<Return>", self.entryCommand)
		self.entry.grid(row = 0, column = 1, sticky = (tkinter.W, tkinter.E), padx = 1.5)

		self.root.grid_rowconfigure(0, weight = 7)
		self.root.grid_rowconfigure(1, weight = 1)
		self.root.grid_columnconfigure(0, weight = 1)
		userInputFrame.grid_rowconfigure(0, weight = 1)
		userInputFrame.grid_columnconfigure(0, weight = 1)
		userInputFrame.grid_columnconfigure(1, weight = 7)

		self.bot = PluginBot(self)
		self.bot.connect()
		self.print("Starting bot main thread.")
		self.bot.start()
		

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
			self.textOutput.see(tkinter.END)


	def sendMessage(self, event):
		if (self.entryMessage != ""):
			if (self.entryMessage[0] == "."):
				self.bot.s.send(BYTE("PRIVMSG %s :%s" % (self.bot.focusedChannel, self.entryMessage)))
				tokenString = "WedrBot PRIVMSG %s :%s" % (self.bot.focusedChannel, self.entryMessage)
				self.bot.handleTokens(self.bot.makeTokens(tokenString))
			else:
				self.bot.s.send(BYTE("PRIVMSG %s :%s" % (self.bot.focusedChannel, self.entryMessage)))
				self.print(text = "<%s> WedrBot: %s" % (self.bot.focusedChannel, self.entryMessage))
			self.textOutput.see(tkinter.END)
			self.entryMessage = ""
			self.entry.delete(0, tkinter.END)

	def getUserInput(self, event):
		self.entryMessage = self.entry.get()
		self.entry.delete(0, tkinter.END)

	def entryCommand(self, event):
		self.getUserInput(event)
		if (self.entryMessage != ""):
			tokens = self.entryMessage.split(" ")
			if (tokens[0] == "/j" or tokens[0] == "/join"):
				#Joining channels
				if (len(tokens) > 2):
					for i in range(1, len(tokens)):
						self.bot.switch(tokens[i])
						self.print("Joining channel %s" % tokens[i])
				elif (len(tokens) == 2):
					self.bot.switch(tokens[1])
					self.print("Joining channel %s" % tokens[1])
				else:
					self.print("Incorrect usage:  /join [channel]")
			elif (tokens[0] == "/q" or tokens[0] == "/e" or tokens[0] == "/quit" or tokens[0] == "/exit"):
				#Quitting the bot client. Make sure to press any keys in the terminal/command prompt after use.
				print("Quitting bot.")
				self.bot.quit()
				self.bot.join()
				print("Quitting tkinter GUI.")
				self.root.destroy()
				return
			elif (tokens[0] == "/c" or tokens[0] == "/clear"):
				#Clearing the text output screen.
				self.textOutput.delete("1.0", tkinter.END)
			elif (tokens[0] == "/r" or tokens[0] == "/reload"):
				#Reloading plugins.
				self.bot.reloadAll()
			elif (tokens[0] == "/l" or tokens[0] == "/leave"):
				#Leaving channels
				if (len(tokens) > 2):
					for i in range(1, len(tokens)):
						self.bot.leave(tokens[i], False)
						self.print("Left channel, %s" % tokens[i])
				elif (len(tokens) == 2):
					self.bot.leave(tokens[1], False)
					self.print("Left channel, %s" % tokens[1])
				else:
					self.print("Incorrect usage:  /leave [channel]")
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


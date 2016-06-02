import tkinter
import tkinter.scrolledtext

class GUI:
	root = None
	textOutput = None

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
		tkinter.Button(master = userInputFrame, text = "Send").grid(row = 0, column = 0, sticky = (tkinter.W, tkinter.E), padx = 1.5)
		tkinter.Entry(master = userInputFrame).grid(row = 0, column = 1, sticky = (tkinter.W, tkinter.E), padx = 1.5)

		self.root.grid_rowconfigure(0, weight = 7)
		self.root.grid_rowconfigure(1, weight = 1)
		self.root.grid_columnconfigure(0, weight = 1)
		userInputFrame.grid_rowconfigure(0, weight = 1)
		userInputFrame.grid_columnconfigure(0, weight = 1)
		userInputFrame.grid_columnconfigure(1, weight = 7)


	def run(self):
		self.root.mainloop()
		print("Hello")

GUI().run()
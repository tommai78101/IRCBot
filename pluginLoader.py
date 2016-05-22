import os
import atexit
import string
import importlib
import threading
from time import sleep

class UserInput(threading.Thread):
	loadedModules = []
	isRunning = False

	def loadModule(self, name):
		return importlib.import_module(name)

	def __init__(self):
		super().__init__()
		directory = os.getcwd()
		pluginFiles = next(os.walk(directory + "/plugins"))[2]
		self.loadedModules.clear()
		for i in range(len(pluginFiles)):
			name = pluginFiles
			module = self.loadModule(str("plugins." + pluginFiles[i])[:-3])
			self.loadedModules.append((name, module))
			print("Loaded plugin %s successfully." % name)
		self.isRunning = False
		self.start()

	def reloadAll(self):
		for i in range(len(self.loadedModules)):
			print("Reloading plugin")
			self.loadedModules[i] = (self.loadedModules[i][0], importlib.reload(self.loadedModules[i][1]))

	def run(self):
		self.isRunning = True
		while (self.isRunning):
			try:
				message = input()
				message = message.split(" ")
				if (message[0] == "/reload"):
					print("Reloading all plugins.")
					self.reloadAll()
				elif (message[0] == "/quit"):
					print("Quitting.")
					self.isRunning = False
			except Exception as error:
				print(error)
		


def main():
	bot = UserInput()
	bot.join()
	

if __name__ == "__main__":
	main()
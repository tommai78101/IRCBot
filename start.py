#This is a unit test script. It should be called outside of the program.
import os
import sys
import pdb
import PluginBot
import threading
import gui
from time import sleep

class WorkerThread(threading.Thread):
	bot = None

	def __init__(self):
		super().__init__()
		self.bot = PluginBot.PluginBot()
		
	def run(self):
		self.bot.run()

	def stopBot(self):
		self.bot.quit()


def main(isTest):
	if (isTest == 0):
		bot = PluginBot.PluginBot()
		bot.connect()
		bot.userInput.join()
		bot.join()
	elif (isTest == 1):
		worker = WorkerThread()
		worker.start()
		print("Sleeping for 3 seconds.")
		sleep(2)
		print("Test reloading plugin.")
		worker.bot.reloadAll()
		print("Sleeping for 2 seconds.")
		sleep(1)
		worker.stopBot()
		print("Success!")
		sleep(1)
	elif (isTest == 2):
		myGUI = gui.GUI()
		myGUI.run()

	
def test():
	value = 0
	for i in range(len(sys.argv)):
		try:
			value = int(sys.argv[i])
		except ValueError:
			value = 0
	main(value)

if (__name__ == "__main__"):
	#pdb.run("test()")
	test()

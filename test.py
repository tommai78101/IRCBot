#This is a unit test script. It should be called outside of the program.
import os
import sys
import PluginBot
import threading
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

if (__name__ == "__main__"):
	worker = WorkerThread()
	worker.start()

	print("Sleeping for 3 seconds.")
	sleep(3)

	print("Reloading plugin.")
	worker.bot.reloadAll()

	print("Sleeping for 2 seconds.")
	sleep(2)

	worker.stopBot()
	print("Success!")

	sys.exit(0)
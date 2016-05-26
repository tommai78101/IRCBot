#This is a unit test script. It should be called outside of the program.
import os
import sys
import pdb
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


def main(isTest):
	if (isTest):
		bot = PluginBot.PluginBot()
		bot.connect()
		bot.userInput.join()
		bot.join()
	else:
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

	
def test():
	checkFlag = True
	for i in range(len(sys.argv)):
		value = sys.argv[i]
		if (value == "1"):
			checkFlag = False
	main(checkFlag)

if (__name__ == "__main__"):
	#pdb.run("test()")
	test()
#This is a unit test script. It should be called outside of the program.

#Default: GUI (parameter value = 0)

#GUI           (Value: 2)     : User-friendly IRC bot client. Simple and minimalistic.
#UNIT-TEST     (Value: 1)     : This is only for unit testing the bot client.
#COMMANDLINE   (Value: 0)     : This is the bare-bone version of the IRC bot client.

#Usage: $> python3 start.py [VALUE]
#Definition:
#	[VALUE]: The parameter value given above.


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


def main(isTest, hostID = -1):
	if (isTest == 0):
		if (bot is None):
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
		myGUI = gui.GUI(hostID)
		myGUI.run()

	
def test():
	value = 2
	hostID = 3
	for i in range(len(sys.argv)):
		try:
			if (i == 1):
				value = int(sys.argv[i])
				print("Test Value: %d" % value)
			elif (i > 1):
				hostID = int(sys.argv[i])
				print("Host ID Value: %d" % hostID)
		except ValueError:
			value = 2
	if (hostID != -1):
		main(value, hostID)
	else:
		main(value)

#  HostID values:
#     0: Rizon
#     1: EFNet
#     2: Freenode
#     3: PanicBNC
if (__name__ == "__main__"):
	print(sys.argv)
	test()

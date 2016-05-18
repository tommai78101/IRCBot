from IRCBot_updates import UpdateBot
from IRCBot_quotes import QuotesBot
from IRCBot_files import FilesBot

global DEBUG
DEBUG = False

#Global constants
HOST = "irc.rizon.net"
PORT = 6667
if (DEBUG):
	CHANNEL = "#wedrbot"
else:
	CHANNEL = "#3dshacks"

def main():
	bot = FilesBot(HOST, PORT, CHANNEL)
	#bot.setChannels(["#3dshacks"])
	bot.connect()
	bot.run()

main()
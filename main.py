from IRCBot_updates import UpdateBot
from IRCBot_quotes import QuotesBot
from IRCBot_files import FilesBot

#Global constants
HOST = "irc.rizon.net"
PORT = 6667
CHANNEL = "#3dshacks-ot"

def main():
	bot = FilesBot(HOST, PORT, CHANNEL)
	#bot.setChannels(["#3dshacks"])
	bot.connect()
	bot.run()

main()
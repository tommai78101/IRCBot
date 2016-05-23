from datetime import datetime
from time import sleep

def BYTE(message):
	return bytes("%s\r\n" % message, "UTF-8")


def getUser(self, token):
	user = token.strip(":")
	user = user.split("!")[0]
	user = user.split("|")[0]
	return user

def getMessage(self, tokens, startingIndex):
	message = ""
	for i in range(startingIndex, len(tokens)):
		if (i == startingIndex):
			tokens[i] = tokens[i].strip(":")
		message += tokens[i].strip("\x01") + " "
	return message

def plugin_main(s, channel, tokens):
	#s := Parent bot socket object
	#channel := Channel the parent bot is focused on.
	#tokens := Read Buffer tokens passed from parent bot.

	#PING protocol
	#tokens[0] is the command, which is PING.
	#tokens[1] is the sender.
	#PING requires the bot to return PONG.
	if (tokens[0] == "PING"):
		currentDate = datetime.now()
		print("[%02s:%02s] Received PING PONG" % (str(currentDate.hour).zfill(2), str(currentDate.minute).zfill(2)))
		str1 = ("PONG %s" % tokens[1].strip(":"))
		s.send(BYTE(str1))

	#PRIVMSG protocol
	#tokens[0] gets the full user account. This needs to be stripped and splitted out.
	#tokens[1] is the command. PRIVMSG is a command.
	#tokens[2] is the channel or recipient name.
	#tokens[3] is the full message with a leading colon. This needs to be stripped.
	if (len(tokens) > 1 and tokens[1] == "PRIVMSG"):
		if (len(tokens) > 2 and tokens[3] == ":\x01VERSION\x01"):
			print("Sending VERSION")
			s.send(BYTE("NOTICE %s :\x01VERSION WedrBot v1.0\x01" % tokens[0]))
		else:
			caller = getUser(tokens[0])
			message = getMessage(tokens, 3)
			recipient = tokens[2]
			try:
				print("%s: %s" % (caller, message))
			except Exception as error:
				print("Plugin Error: ", error)

	assert True


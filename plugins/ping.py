from datetime import datetime

def BYTE(message):
	return bytes("%s\r\n" % message, "UTF-8")

def version():
	return "Ping - v1.0"

def plugin_main(parent, tokens):
	if (tokens[0] == "PING"):
		currentDate = datetime.now()
		print("[%02s:%02s] Received PING PONG" % (str(currentDate.hour).zfill(2), str(currentDate.minute).zfill(2)))
		str1 = ("PONG %s" % tokens[1].strip(":"))
		parent.s.send(BYTE(str1))
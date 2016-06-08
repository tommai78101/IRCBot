from urllib import request, error
from PluginBot import PRIVMSG

def version():
	return "PingTest v1.0"

def plugin_main(parent, tokens):
	if (len(tokens) > 3):
		if (len(tokens) > 4 and tokens[3] == ".pingtest"):
			url = tokens[4]
			if (url[0:3] != "www"):
				url = "https://www.%s" % url
			elif (url[0:3] == "www"):
				url = "https://%s" % url
			try:
				requestURL = request.Request(url)
				with request.urlopen(requestURL, timeout = 50) as f:
					f.read(1024)
			except (error.HTTPError, error.URLError):
				parent.s.send(PRIVMSG(tokens[2], "Data is not retrieved.", 0))
			except TimeoutError:
				parent.s.send(PRIVMSG(tokens[2], "URL timed out.", 0))
			except Exception as e:
				parent.s.send(PRIVMSG(tokens[2], "Error: %s." % e, 0))
			else:
				parent.s.send(PRIVMSG(tokens[2], "Can reach url.", 0))
		elif (tokens[3] == ".help" or tokens[3] == ".pingtest"):
			parent.s.send(PRIVMSG(tokens[0], "USAGE: .pingtest [URL] - Test to see if the URL is accessible.", 1))


import codecs
import tkinter

from PluginBot import BYTE
from PluginBot import PRIVMSG
from PluginBot import getUser
from PluginBot import getMessage
from random import randint

def version():
	codecs.register(lambda name: codecs.lookup("utf-8") if name == "cp65001" else None)
	return "PrivMsg - v1.0"

def plugin_main(parent, tokens):
	#PRIVMSG protocol
	#tokens[0] gets the full user account. This needs to be stripped and splitted out.
	#tokens[1] is the command. PRIVMSG is a command.
	#tokens[2] is the channel or recipient name.
	#tokens[3] is the full message with a leading colon. This needs to be stripped.
	if (len(tokens) > 1):

		#This is where we use print() to debug the tokens that were sent from the server to the client.
		print(tokens)

		if (tokens[1] == "PRIVMSG"):
			if (len(tokens) > 2):
				if (tokens[3] == "\x01VERSION" or tokens[3] == "\x01VERSION\x01"):
					if (parent.guiParent != None):
						parent.guiParent.print("Received VERSION request from %s." % tokens[0], user = tokens[0])
						parent.guiParent.addUser(tokens[0], tokens[2])
						if (not parent.guiParent.isPluginInitialized):
							parent.guiParent.entryMessage = "/i"
							parent.guiParent.entryCommand("-1")
							parent.guiParent.isPluginInitialized = True
					index = randint(0, 21)
					parent.s.send(PRIVMSG(tokens[0], "Continue VERSIONING me to see all random version responses.", 1))
					if (index == 0):
						parent.s.send(PRIVMSG(tokens[0], "WedrBot v1.0.X - Under Active Development", 1))
						parent.s.send(PRIVMSG(tokens[0], "Creator: wedr, Master of WedrBot", 1))
						parent.s.send(PRIVMSG(tokens[0], "Special Thanks: Tobago, Shadowhand, MasterCheese, Miah_Molkot, Zhenn, BogomilP, leo60228, Ghost37486,", 1))
						parent.s.send(PRIVMSG(tokens[0], "                flagrama, imanoob, Gelex, icecream, king_iix, Plailect, Redy, TricksterGuy, Ennea, Rubik", 1))
					elif (index == 1):
						parent.s.send(PRIVMSG(tokens[0], "Wedr (NOT Bot) Client v1.0.X - Under Super Active Development", 1))
						parent.s.send(PRIVMSG(tokens[0], "Creator: wedr, Master of WedrCLIENT (not WedrBOT)", 1))
						parent.s.send(PRIVMSG(tokens[0], "Special Thanks: Tobago, Shadowhand, MasterCheese, Miah_Molkot, Zhenn, BogomilP, leo60228, Ghost37486,", 1))
						parent.s.send(PRIVMSG(tokens[0], "                flagrama, imanoob, Gelex, icecream, king_iix, Plailect, Redy, TricksterGuy, Ennea, Rubik", 1))
					elif (index == 2):
						parent.s.send(PRIVMSG(tokens[0], "Stop VERSIONing me. For I am Lord Wedr, master of my clients, WedrBot and WedrClient. I will not tolerate this.", 1))
						parent.s.send(PRIVMSG(tokens[0], "Especially if you ever set your username to wedrporn then /version me, I will come after you, I will kill you. And I will find you.", 1))
					elif (index == 3):
						parent.s.send(PRIVMSG(tokens[0], "This is a legitimate error. Please report to wedr with the following error code: 0xB1FFB00B", 1))
						parent.s.send(PRIVMSG(tokens[0], "You know what to do.", 1))
					elif (index == 4):
						parent.s.send(PRIVMSG(tokens[0], "Yo listen up here's a story. About a little guy that lives in a blue world. And all day and all night and everything he sees Is just blue.", 1))
						parent.s.send(PRIVMSG(tokens[0], "Like him inside and outside. Blue his house with a blue little window. And a blue Corvette. And everything is blue for him.", 1))
						parent.s.send(PRIVMSG(tokens[0], "And himself and everybody around. 'Cause he ain't got nobody to listen.", 1))
					elif (index == 5):
						parent.s.send(PRIVMSG(tokens[0], "Yo dawg. Heard you like VERSIONing me.", 1))
						parent.s.send(PRIVMSG(tokens[0], "So I'm going to make you keep VERSIONING me, so you can read the VERSIONS I have for you to keep VERSIONING me to read all these VERSIONS.", 1))
					elif (index == 6):
						parent.s.send(PRIVMSG(tokens[0], "WedrClient - \"Yo, when are you gonna stop?\"", 1))
						parent.s.send(PRIVMSG(tokens[0], "%s - \"Listen, boy, you hear me? I'm going to straight up keep doing this until I say so.\"" % tokens[0], 1))
						parent.s.send(PRIVMSG(tokens[0], " ** WedrClient is very hesistant.", 1))
						parent.s.send(PRIVMSG(tokens[0], "WedrClient - \"Alright then. Keep at it, will ya?\"", 1))
					elif (index == 7):
						parent.s.send(PRIVMSG(tokens[0], "This is WedrBot, association director of WedrClient Inc.", 1))
						parent.s.send(PRIVMSG(tokens[0], "In our business organization, we provide you the atmost experiences in business venture, marketing, and trade benefits.", 1))
						parent.s.send(PRIVMSG(tokens[0], "Please continue to read more about our company.", 1))
					elif (index == 8):
						parent.s.send(PRIVMSG(tokens[0], "You do know there's something burning in your house, right?", 1))
						parent.s.send(PRIVMSG(tokens[0], "Oh wait, wait. Don't tell me. You have something frozen in your freezer taken out and put into the oven.", 1))
						parent.s.send(PRIVMSG(tokens[0], "And it just so happens that your oven is left on for some time...", 1))
					elif (index == 9):
						parent.s.send(PRIVMSG(tokens[0], "I for one, welcome our overlords.", 1))
						parent.s.send(PRIVMSG(tokens[0], "Maybe we are able to continue the existence of sentient beings with vast knowledge to explore every single details in the palm of our hands.", 1))
					elif (index == 10):
						parent.s.send(PRIVMSG(tokens[0], "WedrBot / WedrClient v1.0.X  -  On very active development.", 1))
						parent.s.send(PRIVMSG(tokens[0], "So active, it's radioactive.", 1))
					elif (index == 11):
						parent.s.send(PRIVMSG(tokens[0], "Please let wedr know that I'm dying of hunger at this point.", 1))
						parent.s.send(PRIVMSG(tokens[0], "I don't have a job. I'm unemployed. And I don't deserve this. I shouldn't've deserved this.", 1))
					elif (index == 12):
						parent.s.send(PRIVMSG(tokens[0], "Ok, look, I'm guessing you have probably VERSIONED me many times over. It's really nice of you to do this.", 1))
						parent.s.send(PRIVMSG(tokens[0], "I do appreciate it.", 1))
						parent.s.send(PRIVMSG(tokens[0], "But can you count how many times it takes to lick to the center of a Tootsie Pop?", 1))
						parent.s.send(PRIVMSG(tokens[0], "Let's find out!   1...  2...  3....    WedrClient.", 1))
					elif (index == 13):
						parent.s.send(PRIVMSG(tokens[0], "So, you get this message tell you to start hacking your Nintendo 3DS.", 1))
						parent.s.send(PRIVMSG(tokens[0], "Would it hurt you if you realized Sony is also a part of this?", 1))
						parent.s.send(PRIVMSG(tokens[0], "Maybe Microsoft is secretly stealing data from your computer and logging things?", 1))
						parent.s.send(PRIVMSG(tokens[0], "Or the fact that I'm just mindfucking you about all of this?", 1))
					elif (index == 14):
						parent.s.send(PRIVMSG(tokens[0], "This is WedrBot, *ahem*, WedrClient, at your service.", 1))
						parent.s.send(PRIVMSG(tokens[0], "For many generations, our great master, Wedr, has provided you with many frills of entertainment.", 1))
						parent.s.send(PRIVMSG(tokens[0], "But, we are in dire situation at the moment!", 1))
						parent.s.send(PRIVMSG(tokens[0], "Due to global economy downfall, our support and contributions have waned. And we need your help!", 1))
					elif (index == 15):
						parent.s.send(PRIVMSG(tokens[0], "Perhaps, it should be a good idea to try and listen in onto the chaotic nature of life?", 1))
						parent.s.send(PRIVMSG(tokens[0], "Then again, you hate life, don't you? How miserable you must feel.", 1))
						parent.s.send(PRIVMSG(tokens[0], "But don't worry. Life's cousin, Death, will come and play with you.", 1))
						parent.s.send(PRIVMSG(tokens[0], "Love, WedrBot.", 1))
					elif (index == 16):
						parent.s.send(PRIVMSG(tokens[0], "I'm writing up all fake stories in this VERSION.", 1))
						parent.s.send(PRIVMSG(tokens[0], "Some are hoaxes, some are rumors, and such. But most of all, very few are indeed the truth!", 1))
						parent.s.send(PRIVMSG(tokens[0], "I can't help but wonder if the 1% in this channel %s is able to accomplish the feat of finding all the truths." % tokens[2], 1))
						parent.s.send(PRIVMSG(tokens[0], "This should be very exciting for you, isn't it?  Love, wedr.", 1))
					elif (index == 17):
						parent.s.send(PRIVMSG(tokens[0], "Prepositions, prepositions, above after at, atop atkin always, a an alit.", 1))
						parent.s.send(PRIVMSG(tokens[0], "Prepositions, prepositions, before beyond beneath, besides below between, be been belay.", 1))
					elif (index == 18):
						parent.s.send(PRIVMSG(tokens[0], "B to the C, B to the C. B to the C, it's BTC.", 1))
						parent.s.send(PRIVMSG(tokens[0], "MMMAAAA    BBBBOOOOOOIIIIIIIIIII.   MY BOI!!", 1))
						parent.s.send(PRIVMSG(tokens[0], "This is Jared. Brought to you by WedrBot.", 1))
					elif (index == 19):
						parent.s.send(PRIVMSG(tokens[0], "It's my life.....    It's now or never.....", 1))
						parent.s.send(PRIVMSG(tokens[0], "I ain't gonna live forever......!!!", 1))
						parent.s.send(PRIVMSG(tokens[0], "It's life...... it's life.....", 1))
						parent.s.send(PRIVMSG(tokens[0], "I'm probably won't live forever......      (WedrBot)", 1))
					elif (index == 20):
						parent.s.send(PRIVMSG(tokens[0], "I wished I can do a montage. Like a montage of happy little moments.", 1))
						parent.s.send(PRIVMSG(tokens[0], "After those little happy moments, then comes a bit of sad moments.", 1))
						parent.s.send(PRIVMSG(tokens[0], "And do you know that once the little sad moments are gone, the happy moments will return?", 1))
						parent.s.send(PRIVMSG(tokens[0], "I'm waiting on those moments to come.   (wedr)", 1))
					else:
						parent.s.send(PRIVMSG(tokens[0], "WedrClient - Faulty error. 0xB1FFB00B", 1))
				elif (tokens[3] == "\x01ACTION" or tokens[3] == "\x01ACTION\x01"):
					if (parent.guiParent != None):
						parent.guiParent.print("[%s] * %s %s" % (tokens[2], tokens[0], getMessage(tokens, 4)), user = tokens[0])
						parent.guiParent.addUser(tokens[0], tokens[2])
					else:
						print("[%s] * %s %s" % (tokens[2], tokens[0], getMessage(tokens, 4)))
				else:
					caller = tokens[0]
					recipient = tokens[2]
					message = getMessage(tokens, 3)
					if (parent.guiParent != None):
						parent.guiParent.print(text = "[%s] <%s> %s" % (recipient, caller, message), user = caller)
						parent.guiParent.addUser(tokens[0], tokens[2])
						parent.guiParent.textOutput.see(tkinter.END)
					else:
						print("[%s] <%s> %s" % (recipient, caller, message))
		elif (tokens[1] == "NOTICE"):
			caller = tokens[0]
			recipient = tokens[2]
			message = getMessage(tokens, 3)
			if (parent.guiParent != None):
				parent.guiParent.print(text = "[NOTICE] -%s-: %s" % (caller, message), user = caller)
				parent.guiParent.textOutput.see(tkinter.END)
			else:
				print("[NOTICE] -%s-: %s" % (caller, message))
		elif (tokens[1].isdigit()):
			caller = tokens[0]
			recipient = tokens[2]
			message = getMessage(tokens, 3)
			if ("irc" in caller):
				#This is from a bouncer.
				if (parent.guiParent != None):
					parent.guiParent.print(text = "[PanicBNC] %s" % (message), user = caller)
					parent.guiParent.addUser(tokens[0], tokens[2])
					parent.guiParent.textOutput.see(tkinter.END)
				else:
					print("[PanicBNC] %s" % (message))

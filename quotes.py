import xchat
from datetime import date
from random import choice

__module_name__ = "Quotes"
__module_version__ = "1.0"
__module_description__ = "Adds a quote to a database"

quoteDB = "/home/local/ANT/tobialee/quotes.txt"
quotes = []

def loadQuotes():
	global quoteDB
	global quotes
	file = open(quoteDB, "r")
	for line in file:
		index = line.find(' ')
		date = line[:index]
		words = line[index+1:]
		index = words.find(' ')
		name = words[:index]
		words = words[index+1:]
		quotes = quotes + [(date, name, words)]
	file.close()
	xchat.prnt(str(len(quotes)) + " Quotes loaded")

def reloadQuotes():
	global quotes
	global quoteDB
	quotes = []
	loadQuotes()
	xchat.command("say Quotes reloaded")

def addquote(word, quote):
	global quotes
	name = word[0]
	year = str(date.today().year)
	month = str(date.today().month)
	if len(month) == 1:
		month = "0" + month
	day = str(date.today().day)
	if len(day) == 1:
		day = "0" + day
	
	today = year + "-" + month + "-" + day
	toadd = (today, name, quote)
	quotes = quotes + [toadd]
	file = open(quoteDB, "a")
	file.write(today + " " + name + " " + quote + "\n")
	file.close() 
	xchat.command("say Quote #" + str(len(quotes)) + " added")

def readquote(number):
	global quotes
	global muted
	if muted:
		return
	if number[0] == "#":
		number = number[1:]
	if int(number) <= 0:
		return
	try:
		quote = quotes[int(number)-1]
		xchat.command("say Quote #" + str(number) + " added by " + quote[1] + " on " + quote[0] + ": " + quote[2])
	except:
		xchat.command("say Error reading quote")

def dumpquotes():
	global quotes
	file = open("quotedump.txt", "w")
	num = 1
	for quote in quotes:
		file.write("Quote #" + str(num) + " added by " + quote[1] + " on " + quote[0] + ": " + quote[2])
		num = num + 1
	xchat.command("say Quotes written to file")
	file.close()

def findquote(string):
	global quotes
	global muted
	if muted:
		return
	list = []
	index = 1
	for i in quotes:
		if string.lower() in str(i[2]).lower():
			list = list + ["#"+str(index)]
		index = index + 1
	if len(list) == 0:
		xchat.command("say No quotes found")
	elif len(list) == 1:
		readquote(list[0])
	else:
		total = ", ".join(list)
		xchat.command("say Quotes found: " + total)

def help(name):
	xchat.command("notice " + name + " Commands: add, read, reload, random, help")

def quotes_cb(word, word_eol, userdata):
	global quotes
	global muted
	argument = word[1]
	if argument[:7].lower() == ".quote ":
		argument = argument[7:]
		if argument[:4].lower() == "add ":
			addquote(word, argument[4:])
		elif argument[:5].lower() == "read ":
			readquote(argument[5:])
		elif argument[:6].lower() == "reload":
			if word[0] == "tobialee":
				reloadQuotes()
		elif argument[:6].lower() == "random":
			readquote(str(choice(range(len(quotes)))+1))
		elif argument[:7].lower() == "search ":
			findquote(argument[7:])
		elif argument[:4].lower() == "help":
			help(word[0])
		elif argument[:4].lower() == "dump":
			if word[0] == "tobialee":
				dumpquotes()
	return xchat.EAT_NONE

def pm_cb(word, word_eol, userdata):
	global muted
	global ops
	if word[0].lower() in ops:
		if word[1][0:4] == "mute":
			muted = True
			chan = xchat.find_context(channel="#interns")
			chan.command("say Muted")
			xchat.command("msg " + word[0] + " Muted")
		elif word[1][0:6] == "unmute":
			muted = False
			chan = xchat.find_context(channel="#interns")
			chan.command("say Unmuted")
			xchat.command("msg " + word[0] + " Unmuted")
	return xchat.EAT_NONE

muted = False
loadQuotes()
ops = ["tobialee", "jzanutto", "zanuttoj", "T_T", "^_^"]
xchat.hook_print("Channel Message", quotes_cb)
xchat.hook_print("Channel Msg Hilight", quotes_cb)
xchat.hook_print("Private Message to Dialog", pm_cb)

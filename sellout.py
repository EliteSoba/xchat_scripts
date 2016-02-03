__module_name__ = "Sellout" 
__module_version__ = "1.1a" 
__module_description__ = "Sells out" 

import xchat
import time

whitelist = ["monotonetim"]

def sellout_cb(word, word_eol, userdata):
	global valid
	global link
	global enabled

	#chan = xchat.find_context(channel="#not_tim")
	#if chan is None:
	#	return xchat.EAT_NONE

	words = word[1].split(' ')
	# Will always have at least one element of words
	if not words[0] == "!sellout":
		return xchat.EAT_NONE
	
	if len(words) > 1:
		if len(word) >= 3 and word[2] == "@":
			if words[1] == "on":
				if not enabled:
					xchat.command("say Selling out turned on")
				enabled = True
			elif words[1] == "off":
				if enabled:
					xchat.command("say Selling out turned off")
				enabled = False
			elif "amazon.com" in words[1]:
				the_link = ' '.join(words[1:])
				xchat.command("say Associates link changed to: " + the_link)
				
				file = open(link, "w")
				file.write(the_link)
				file.close()
			elif valid and enabled:
				file = open(link, "r")
				the_link = file.readline()
				file.close()
				
				xchat.command("say Amazon Associates Link: " + the_link)
				valid = False
				timer = xchat.hook_timer(60000, timer_cb)
		else:
			if valid and enabled:
				file = open(link, "r")
				the_link = file.readline()
				file.close()
				
				xchat.command("say Amazon Associates Link: " + the_link)
				valid = False
				timer = xchat.hook_timer(60000, timer_cb)
	else:
		if valid and enabled:
				file = open(link, "r")
				the_link = file.readline()
				file.close()
				
				xchat.command("say Amazon Associates Link: " + the_link)
				valid = False
				timer = xchat.hook_timer(60000, timer_cb)
	
	return xchat.EAT_NONE

def changelink_cb(word, word_eol, userdata):
	global whitelist
	global link
	if word[0] not in whitelist:
		if len(word) <3:
			return xchat.EAT_NONE
		if word[2] != "@":
			return xchat.EAT_NONE

	words = word[1].split(' ')
	# Will always have at least one element of words
	if not words[0] == "!setlink":
		return xchat.EAT_NONE
	
	the_link = ' '.join(words[1:])
	xchat.command("say Associates link changed to: " + the_link)
	
	file = open(link, "w")
	file.write(the_link)
	file.close()
		
	return xchat.EAT_NONE

def timer_cb(userdata):
	global valid
	valid = True
	return 0

valid = True
enabled = True
link = "link.txt"
xchat.hook_print("Channel Message", changelink_cb)
xchat.hook_print("Channel Message", sellout_cb)
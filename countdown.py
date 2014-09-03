__module_name__ = "Countdown" 
__module_version__ = "1.0" 
__module_description__ = "Counts down from the specified number" 

import xchat
import time

def countdown_cb(word, word_eol, userdata):
	global max
	global valid
	
	nick = word[0][1:]
	while len(nick) > 0 and nick[0].isdigit():
		nick = nick[1:]
	
	if nick != "Elite_Soba" and nick != "jdp":
		return xchat.EAT_NONE
	
	#if word[0] == "Orcus" or word[0] == "Violent_Semen_Inferno":
	#	return xchat.EAT_NONE
	#if word[2] != "&" and not valid:
	#	return xchat.EAT_NONE
	if word[2] == "@" or word[2] == "~" or word[2] == "&":
		words = word[1].split(' ')
		# Will always have at least one element of words
		if not words[0] == ".countdown":
			return xchat.EAT_NONE
		if len(words) != 2:
			xchat.command("say Usage: .countdown x || Count down for x seconds (limit " + str(max) + ")")
			return xchat.EAT_NONE
		if not words[1].isdigit():
			xchat.command("say Usage: .countdown x || Count down for x seconds (limit " + str(max) + ")")
			return xchat.EAT_NONE
		if int(words[1]) > max:
			xchat.command("say Error: Please use a number no greater than " + str(max) + " for now")
			return xchat.EAT_NONE
		#valid = False
		for i in reversed(range(int(words[1]))):
			xchat.command("say " + str(i+1))
			time.sleep(1)
		#timer = xchat.hook_timer(1800000, timer_cb)
	return xchat.EAT_NONE

def timer_cb(userdata):
	valid = True
	return 0

max = 3
valid = True
xchat.hook_print("Channel Message", countdown_cb)
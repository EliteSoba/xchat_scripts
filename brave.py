__module_name__ = "BRAVE"
__module_version__ = "1.0"
__module_description__ = "Be braaaaave"

import xchat
import random

swears = ["SHITASSES", "ASSHOLES", "SHOCKSUCKERS", "YOU COCKSUCKERS", "DIPSHITS", "SHITTERS", "TURDS", "SHITHEADS", "PILE OF SHITS", "PRICKS", "HORSES ASSES", "BLOODY BASTARDS", "SON OF A BITCHES", "MOTHAFUCKAS", "FUCKERS", "YOU STINKERS", "YOU QUACKS"]

def brave_cb(word, word_eol, userdata):
	global swears
	global valid
	
	if not valid:
		return xchat.EAT_NONE
	
	words = word[1].split(' ')
	# Will always have at least one element of words
	if not words[0] == "!brave":
		return xchat.EAT_NONE
	
	string = "BE BRAVE " + random.choice(swears)
	
	xchat.command("say " + string)
	valid = False
	timer = xchat.hook_timer(10000, timer_cb)
	return xchat.EAT_NONE

def timer_cb(userdata):
	global valid
	valid = True
	return 0

valid = True
xchat.hook_print("Channel Message", brave_cb)
import xchat
import random

__module_name__ = "Choose"
__module_version__ = "1.01"
__module_description__ = "Chooses from a comma separated list"

def choose_cb(word, word_eol, userdata):
	global C_Enabled
	if not C_Enabled:
		return xchat.EAT_NONE
	if word[1][0:3] == ".c ":
		options = word[1][3:].split(" ")
		if "," in word[1][3:]:
			options = word[1][3:].split(",")
		choice = random.choice(options)
		xchat.command("say " + word[0] + ": " + choice.strip())
	return xchat.EAT_NONE
	
	
def en_cb(word, word_eol, userdata):
	global C_Enabled
	if word[0].lower() == "tobialee":
		if word[1][0:6] == "enable":
			if word[1][7:9].lower() == ".c":
				C_Enabled = True
				xchat.command("msg tobialee Choose Module enabled")
		elif word[1][0:7] == "disable":
			if word[1][8:10].lower() == ".c":
				C_Enabled = False
				xchat.command("msg tobialee Choose Module disabled")
	return xchat.EAT_NONE


C_Enabled = True
xchat.hook_print("Private Message to Dialog", en_cb)
xchat.hook_print("Channel Message", choose_cb)
xchat.hook_print("Your Message", choose_cb)

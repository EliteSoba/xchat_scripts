__module_name__ = "ignore nswf" 
__module_version__ = "1.0" 
__module_description__ = "Ignores TheKey's NSFW pics" 

import xchat
import urllib2

def checkmessage_cb(word, word_eol, userdata):
	if xchat.nickcmp(xchat.get_info("channel"), "#news") == 0:
		nick = word[0][1:]
		while len(nick) > 0 and nick[0].isdigit():
			nick = nick[1:]
		if nick.lower() == "thekey":
			if "NSFW" in word[1]:
				return xchat.EAT_ALL
	return xchat.EAT_NONE

xchat.hook_print("Channel Message", checkmessage_cb)
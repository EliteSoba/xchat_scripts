__module_name__ = "ignorefind" 
__module_version__ = "1.1" 
__module_description__ = "ignores all @finds and !finds and !lolis and !futas in #news" 

import xchat

def checkmessage_cb(word, word_eol, userdata):
	if xchat.nickcmp(xchat.get_info("channel"), "#news") == 0:
		if word[1][1:5] == "find":
			return xchat.EAT_ALL
		elif word[1][0:5] == "!loli" or word[1][0:5] == "!futa":
			return xchat.EAT_ALL
		else:
			return xchat.EAT_NONE
	return xchat.EAT_NONE

xchat.hook_print("Channel Message", checkmessage_cb)
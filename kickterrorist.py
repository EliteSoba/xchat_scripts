__module_name__ = "kickterrorist" 
__module_version__ = "1.0" 
__module_description__ = "Kicks terrorists from channel" 

import xchat

def checkterror_cb(word, word_eol, userdata):
	if xchat.nickcmp(xchat.get_info("channel"), "#commie-subs") == 0:
		if "EUZUBILLAHIMINE" in word[1]:
			nick = word[0][1:]
			while len(nick) > 0 and nick[0].isdigit():
				nick = nick[1:]
			xchat.command("kickban " + nick)
			return xchat.EAT_NONE
	return xchat.EAT_NONE

xchat.hook_print("Channel Message", checkterror_cb)
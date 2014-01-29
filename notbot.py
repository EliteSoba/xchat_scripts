__module_name__ = "Not a bot" 
__module_version__ = "1.1" 
__module_description__ = "Responds to xdcc requests" 

import xchat

def notbot_cb(word, word_eol, userdata):
	if xchat.nickcmp(xchat.get_info("nick"), "Mafuyu-chan") == 0:
		chan = xchat.find_context(channel="#commie-subs")
		if chan is None:
			return xchat.EAT_NONE
		if str.lower(word[1][0:4]) == "xdcc" or str.lower(word[1][0:5]) == "!find":
			test = "SAY MAFUYU-CHAN IS NOT A BOT " + str.upper(word[0]) + " MAFUYU-CHAN IS NOT ｡･ﾟ･(ﾉД`)･ﾟ･｡ "
			chan.command(test)
			penis = "kick " + word[0]
			chan.command(penis)
			return xchat.EAT_NONE
	return xchat.EAT_NONE

xchat.hook_print("Private Message to Dialog", notbot_cb)
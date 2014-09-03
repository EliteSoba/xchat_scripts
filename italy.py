__module_name__ = "Fuck Italy" 
__module_version__ = "1.0" 
__module_description__ = "Italy is not a real country" 

import xchat

channel_name = "#commie-subs"
joined = []
ciao = []

def join_cb(word, word_eol, userdata):
	global joined
	global channel_name
	
	if xchat.nickcmp(xchat.get_info("channel"), channel_name) != 0:
		return xchat.EAT_NONE
		
	joined.append(xchat.strip(word[0]))
	return xchat.EAT_NONE

def italy_cb(word, word_eol, userdata):
	global joined
	global ciao
	global channel_name
	
	if xchat.nickcmp(xchat.get_info("channel"), channel_name) != 0:
		return xchat.EAT_NONE
	chan = xchat.find_context(channel=channel_name)
		
	if not (xchat.strip(word[0]) in joined or xchat.strip(word[0]) in ciao):
		return xchat.EAT_NONE
		
	if xchat.strip(word[0]) in joined:
		joined.remove(xchat.strip(word[0]))
		if word[1] == "ciao":
			ciao.append(xchat.strip(word[0]))
		return xchat.EAT_NONE
	
	if xchat.strip(word[0]) in ciao:
		ciao.remove(xchat.strip(word[0]))
		if word[1] == "!list":
			chan.command("kickban " + xchat.strip(word[0]) + " Italians aren't real people")
			
	return xchat.EAT_NONE

xchat.hook_print("Join", join_cb)
xchat.hook_print("Channel Message", italy_cb)
__module_name__ = "pomf" 
__module_version__ = "1.1" 
__module_description__ = "pomf =3" 

import xchat

def pomf_cb(word, word_eol, userdata):
	chan = xchat.find_context(channel="#commie-subs")
	if chan is None:
		return xchat.EAT_NONE
	if xchat.get_info("nick").lower() == "pomf":
		words = word[1].split(' ')
		for i in range(len(words)-3):
			if words[i].lower() == "do" and words[i+1].lower() == "on" and words[i+2].lower() == "the" and words[i+3][0:3].lower() == "bed":
				xchat.command("me =3")
				return xchat.EAT_NONE
	return xchat.EAT_NONE

xchat.hook_print("Channel Message", pomf_cb)
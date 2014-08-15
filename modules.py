import xchat

__module_name__ = "Modules"
__module_version__ = "1.1"
__module_description__ = "Re/un/loads modules via PM"

def pm_cb(word, word_eol, userdata):
	if word[0].lower() == "tobialee":
		if word[1][0:7] == "reload ":
			xchat.command("py reload " + word[1][7:])
			xchat.command("msg " + word[0] + " " + word[1][7:] + " reloaded")
		elif word[1][0:5] == "load ":
			xchat.command("py load " + word[1][5:])
			xchat.command("msg " + word[0] + " " + word[1][5:] + " loaded")
		elif word[1][0:7] == "unload ":
			xchat.command("py unload " + word[1][7:])
			xchat.command("msg " + word[0] + " " + word[1][7:] + " unloaded")
	return xchat.EAT_NONE

xchat.hook_print("Private Message to Dialog", pm_cb)

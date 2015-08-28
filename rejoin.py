__module_name__ = "Unban/Rejoin" 
__module_version__ = "1.0" 
__module_description__ = "Unbans self from channel and rejoins automatically" 

import xchat
import time

def banned_cb(word, word_eol, userdata):
	channel = word[0]
	timer = xchat.hook_timer(3000, timer_cb, channel)
	return xchat.EAT_NONE

def timer_cb(channel):
	xchat.command("msg chanserv unban " + channel + " " + xchat.get_info("nick"))
	time.sleep(1)
	xchat.command("join " + channel)
	return 0

xchat.hook_print("Banned", banned_cb)
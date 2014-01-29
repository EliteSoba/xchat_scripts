__module_name__ = "Nyaa title" 
__module_version__ = "1.0" 
__module_description__ = "Prints the name of a nyaa torrent" 

import xchat
from urlparse import urlparse
import lxml.html

def nyaa_cb(word, word_eol, userdata):
	chan = xchat.find_context(channel="#commie-subs")
	if chan is None:
		return xchat.EAT_NONE
	for url in word[1].split(' '):
		o = urlparse(url)
		if o.netloc is '':
			continue
		else:
			s = o.netloc.lower().split('.')
			for part in s:
				if part == "nyaa":
					t = lxml.html.parse(url)
					title = t.find(".//title").text
					if title.split(" >> ")[1] == "Unknown ID":
						return xchat.EAT_NONE
					chan.command("say Torrent Name: " + title.split(" >> ")[1])
					return xchat.EAT_NONE
	return xchat.EAT_NONE

xchat.hook_print("Channel Message", nyaa_cb)
__module_name__ = "YouTube title" 
__module_version__ = "1.13" 
__module_description__ = "Prints the name of a YouTube Video" 

import xchat
from urlparse import urlparse
import gdata.youtube
import gdata.youtube.service

def yt_cb(word, word_eol, userdata):
	chan = xchat.find_context(channel="#commie-subs")
	if not YT_enabled:
		return xchat.EAT_NONE
	if chan is None:
		return xchat.EAT_NONE
	for url in word[1].split(' '):
		o = urlparse(url)
		if o.netloc is '':
			continue
		else:
			s = o.netloc.lower().split('.')
			for part in s:
				if part == "youtube" or part == "youtu":
#					vid = url[url.find('v=')+2:]
#					if vid.find('&') != -1
#						vid = vid[:vid.find('&')]
					vid = url[url.find('v=')+2:url.find('v=')+13]
					service = gdata.youtube.service.YouTubeService()
					try:
						entry = service.GetYouTubeVideoEntry(video_id=vid)
					except gdata.service.RequestError:
						xchat.prnt("Invalid Video ID")
						return xchat.EAT_NONE
					title = entry.media.title.text
					chan.command("say YouTube video title: " + title)
					return xchat.EAT_NONE
	return xchat.EAT_NONE

def en_cb(word, word_eol, userdata):
	global YT_Enabled
	if word[0].lower() == "elite_soba":
		if word[1][0:6] == "enable":
			if word[1][7:9].lower() == "yt":
				YT_enabled = True
				xchat.command("msg Elite_Soba YT Module enabled")
		elif word[1][0:7] == "disable":
			if word[1][8:10].lower() == "yt":
				YT_enabled = False
				xchat.command("msg Elite_Soba YT Module disabled")
	return xchat.EAT_NONE


YT_enabled = True
xchat.hook_print("Channel Message", yt_cb)
xchat.hook_print("Private Message to Dialog", en_cb)
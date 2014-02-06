__module_name__ = "YouTube title" 
__module_version__ = "1.01" 
__module_description__ = "Prints the name of a YouTube Video" 

import xchat
from urlparse import urlparse
import gdata.youtube
import gdata.youtube.service

def yt_cb(word, word_eol, userdata):
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
				if part == "youtube" or part == "youtu":
#					vid = url[url.find('v=')+2:]
#					if vid.find('&') != -1
#						vid = vid[:vid.find('&')]
					vid = url[url.find('v=')+2:url.find('v=')+13]
					try:
						entry = service.GetYouTubeVideoEntry(video_id=vid)
					except gdata.service.RequestError:
						xchat.prnt("Invalid Video ID")
						return xchat.EAT_NONE
					title = entry.media.title.text
					chan.command("say YouTube Video Name: " + title)
					return xchat.EAT_NONE
	return xchat.EAT_NONE

service = gdata.youtube.service.YouTubeService()
xchat.hook_print("Channel Message", yt_cb)
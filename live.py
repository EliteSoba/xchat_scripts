__module_name__ = "Live Channel Detector"
__module_version__ = "1.0"
__module_description__ = "A bot that will tell you when a channel goes live"

import xchat
import urllib
import urllib2
import json
import time
import winsound

def check_live(name):
	url = "https://api.twitch.tv/kraken/streams/" + name
	req = urllib2.Request(url, headers = {"Accept" : "application/vnd.twitch.tv.v2+json"})
	response = urllib2.urlopen(req)
	data = response.read()
	decoded = json.loads(data)
	return decoded["stream"] != None

live = False
	
while True:
	result = check_live("monotonetim")
	if not live and result:
		live = True
		winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
	elif live and not result:
		live = False
	time.sleep(1)
__module_name__ = "Live Channel Detector"
__module_version__ = "0.7"
__module_description__ = "A script that will tell you when a channel goes live"

#TODO: Add a way to stop monitoring a stream other than unloading the plugin
#TODO: Also, changing the sound playing to be more universal
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

def monitor_cb(word, word_eol, userdata):
	if len(word) < 2: 
		print "Second arg must be the channel!" 
	else:
		channel = word_eol[1]
		xchat.prnt("Monitoring for channel " + channel + " is now active")
		timer = xchat.hook_timer(1000, timer_cb, channel)
	return xchat.EAT_ALL
	
def timer_cb(channel):
	global live
	result = check_live(channel)
	if not live and result:
		live = True
		winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
		xchat.prnt(channel + " is now live")
	elif live and not result:
		live = False
		xchat.prnt(channel + " is no longer live")
	return 1

xchat.hook_command("monitor", monitor_cb, help = "/MONITOR <channel> Alerts when the desired channel is live")
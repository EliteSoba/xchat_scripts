__module_name__ = "Tim Monitor"
__module_version__ = "1.11"
__module_description__ = "A bot that will tell you if Tim is streaming on any channel"

import xchat
import urllib
import urllib2
import json
import time
import winsound

#Checks if a Twitch stream is live. Note that there is a slight delay in Twitch's API
def check_twitch(name):
	url = "https://api.twitch.tv/kraken/streams/" + name
	req = urllib2.Request(url, headers = {"Accept" : "application/vnd.twitch.tv.v2+json"})
	response = urllib2.urlopen(req)
	data = response.read()
	decoded = json.loads(data)
	return decoded["stream"] != None

#Checks if a Hitbox stream is live
def check_hitbox(name):
	url = "http://hitbox.tv/api/media/status/" + name
	response = urllib2.urlopen(url)
	data = response.read()
	decoded = json.loads(data)
	return decoded["media_is_live"] == '1'

#Key = Channel. Value = tuple of (Liveness, On Twitch)
monitoring = {"monotonetim" : (False, True), "acetonetim" : (False, True), "stereotonetim" : (False, True), "thepuyoplace" : (False, False)}
monitor = False

def monitor_cb(word, word_eol, userdata):
	global monitor
	monitor = True
	xchat.prnt("Monitoring started")
	timer = xchat.hook_timer(1000, twitch_cb)
	return xchat.EAT_ALL

def unmonitor_cb(word, word_eol, userdata):
	global monitor
	monitor = False
	xchat.prnt("Monitoring stopped")
	return xchat.EAT_ALL
	
def twitch_cb(userdata):
	global monitoring
	global monitor
	
	if not monitor:
		return 0
	
	#Check the status of all monitored channels
	for channel in monitoring:
		try:
			live = monitoring[channel][0]
			result = False
			if monitoring[channel][1]:
				result = check_twitch(channel)
			else:
				result = check_hitbox(channel)
			
			#If we think about liveness as a clock, we only care about rising and falling edges
			#so we must continue monitoring even after the channel goes live
			
			#If the channel was not live before and is live now,
			#change the status in the dictionary and alert user
			if not live and result:
				monitoring[channel] = (True, monitoring[channel][1])
				xchat.command("say " + channel + " is now live on " + ("Twitch at twitch.tv/" if monitoring[channel][1] else "Hitbox at hitbox.tv/") + channel)
			#If the channel was live before and is not now,
			#change the status in the dictionary and also alert user
			elif live and not result:
				monitoring[channel] = (False, monitoring[channel][1])
				xchat.prnt(channel + " is no longer live")
		except urllib2.URLError:
			xchat.prnt("Error checking stream status. Connection likely timed out")
	return 1

xchat.hook_command("monitor", monitor_cb, help = "/MONITOR Alerts when Tim is live")
xchat.hook_command("unmonitor", unmonitor_cb, help = "/UNMONITOR Stop monitoring")
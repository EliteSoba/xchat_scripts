__module_name__ = "Live Channel Detector"
__module_version__ = "1.0"
__module_description__ = "A script that will tell you when a channel goes live"

#DONE: Add a way to stop monitoring a stream other than unloading the plugin
#TODO: Also, changing the sound playing to be more universal
#DONE: Add a command to see all the streams you're currently monitoring?
#DONE(?): Also handle this exception:
"""
 Traceback (most recent call last):
   File "C:\Program Files\XChat-WDK\plugins\live.py", line 36, in timer_cb
     result = check_live(channel)
   File "C:\Program Files\XChat-WDK\plugins\live.py", line 18, in check_live
     response = urllib2.urlopen(req)
   File "C:\Python27\Lib\urllib2.py", line 126, in urlopen
     return _opener.open(url, data, timeout)
   File "C:\Python27\Lib\urllib2.py", line 394, in open
     response = self._open(req, data)
   File "C:\Python27\Lib\urllib2.py", line 412, in _open
     '_open', req)
   File "C:\Python27\Lib\urllib2.py", line 372, in _call_chain
     result = func(*args)
   File "C:\Python27\Lib\urllib2.py", line 1207, in https_open
     return self.do_open(httplib.HTTPSConnection, req)
   File "C:\Python27\Lib\urllib2.py", line 1174, in do_open
     raise URLError(err)
 urllib2.URLError: <urlopen error [Errno 10054] An existing connection was forcibly closed by the remote host>
"""
#TODO: Also maybe make it have an option to automonitor whoever you're following
#TODO: Allow for adjustable monitoring frequency?
#TODO: Hell, just turn this into a desktop application, I guess. Pull out the C++
import xchat
import urllib
import urllib2
import json
import time
import winsound

#Checks if a stream is live or not. Note that there is a slight delay in Twitch's API
def check_live(name):
	url = "https://api.twitch.tv/kraken/streams/" + name
	req = urllib2.Request(url, headers = {"Accept" : "application/vnd.twitch.tv.v2+json"})
	response = urllib2.urlopen(req)
	data = response.read()
	decoded = json.loads(data)
	return decoded["stream"] != None

#Key = Channel. Value = Liveness
monitoring = {}

def monitor_cb(word, word_eol, userdata):
	global monitoring
	if len(word) < 2: 
		print "Second arg must be the channel!" 
	else:
		channel = word_eol[1]
		xchat.prnt("Monitoring for channel " + channel + " is now active")
		
		starting = False
		#If monitoring has just started
		if len(monitoring) == 0:
			starting = True
		
		#Add channel to monitoring dictionary. Set liveness default to false.
		monitoring[channel] = False
		
		#Just for some synchronicity safety
		#TODO: This way adds a bit more complexity over just using an if/else
		#and putting the monitoring[] = False in both. Consider changing
		if starting:
			timer = xchat.hook_timer(1000, timer_cb, channel)
	return xchat.EAT_ALL

def unmonitor_cb(word, word_eol, userdata):
	global monitoring
	if len(word) < 2: 
		print "Second arg must be the channel!" 
	else:
		channel = word_eol[1]
		if channel in monitoring:
			del monitoring[channel]
			xchat.prnt("Stopped monitoring channel " + channel)
		else:
			xchat.prnt("Channel " + channel + " was not being monitored to begin with")
	return xchat.EAT_ALL
	
def list_cb(word, word_eol, userdata):
	global monitoring
	
	if len(monitoring) == 0:
		xchat.prnt("You are not monitoring any streams at the moment")
	else:
		xchat.prnt("Monitoring: " + ", ".join(monitoring))
	
	return xchat.EAT_ALL
	
def timer_cb():
	global monitoring
	
	#If monitoring list has become empty
	if len(monitoring) == 0:
		xchat.prnt("No longer monitoring any channels.")
		return 0
	
	#Check the status of all monitored channels
	for channel in monitoring:
		try:
			live = monitoring[channel]
			result = check_live(channel)
			
			#If we think about liveness as a clock, we only care about rising and falling edges
			#so we must continue monitoring even after the channel goes live
			
			#If the channel was not live before and is live now,
			#change the status in the dictionary and alert user
			if not live and result:
				monitoring[channel] = True
				winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
				xchat.prnt(channel + " is now live")
			#If the channel was live before and is not now,
			#change the status in the dictionary and also alert user
			elif live and not result:
				monitoring[channel] = False
				xchat.prnt(channel + " is no longer live")
		except urllib2.URLError:
			xchat.prnt("Error checking stream status. Connection likely timed out")
	return 1

xchat.hook_command("monitor", monitor_cb, help = "/MONITOR <channel> Alerts when the desired channel is live")
xchat.hook_command("unmonitor", unmonitor_cb, help = "/UNMONITOR <channel> Stops monitoring the channel")
xchat.hook_command("mlist", list_cb, help = "/MLIST Lists all the channels currently being monitored")
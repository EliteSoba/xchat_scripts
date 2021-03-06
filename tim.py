﻿__module_name__ = "Tim Monitor"
__module_version__ = "1.53a"
__module_description__ = "A bot that will tell you if Tim is streaming on any channel"

import xchat
import urllib
import urllib2
import json
import sys
import time

class Status:
	online = 1
	offline = 2
	ending = 3

class TimeDelta:
	sec = 0
	min = 0
	hour = 0
	day = 0
	week = 0
	def __init__(self, time):
		self.sec = int(time % 60)
		time = time / 60
		self.min = int(time % 60)
		time = time / 60
		self.hour = int(time % 24)
		time = time / 24
		self.day = int(time % 7)
		self.week = int(time / 7)
	
	def readableTime(self):
		
		time = "It has been "
		if not self.week is 0:
			time = time + str(self.week) + " weeks, "
		if not self.day is 0:
			time = time + str(self.day) + " days, "
		if not self.hour is 0:
			time = time + str(self.hour) + " hours, "
		time = time + str(self.min) + " minutes, "
		time = time + "and " + str(self.sec) + " seconds since the last stream"
		return time
	
lastStreamTime = -1
filename = "laststream.txt"
cooldown = False

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
	try:
		decoded = json.loads(data)
	except ValueError:
		#I'm not completely sure of the specifics because doing this right when someone goes offline
		#is a pain, but when someone goes offline I seem to get an error decoding a JSON object
		return False
	return decoded["media_is_live"] == '1'

#Key = Channel. Value = tuple of (Liveness, On Twitch)
monitoring = {"monotonetim" : (Status.offline, True), "acetonetim" : (Status.offline, True), "stereotonetim" : (Status.offline, True), "thepuyoplace" : (Status.offline, False)}
monitor = False

def monitor_cb(word, word_eol, userdata):
	global monitor
	
	#Don't want to start timer multiple times
	if monitor:
		xchat.prnt("Monitoring is already in progress")
		return xchat.EAT_ALL
	
	monitor = True
	xchat.prnt("Monitoring started")
	timer = xchat.hook_timer(1000, monitoring_cb)
	return xchat.EAT_ALL

def unmonitor_cb(word, word_eol, userdata):
	global monitor
	
	#Not particularly necessary, but still nice to alert the user.
	if not monitor:
		xchat.prnt("Monitoring not in progress")
		return xchat.EAT_ALL
	
	monitor = False
	xchat.prnt("Monitoring stopped")
	return xchat.EAT_ALL
	
def monitoring_cb(userdata):
	global monitoring
	global monitor
	global lastStreamTime
	global filename
	
	if not monitor:
		return 0
	
	#Check the status of all monitored channels
	for channel in monitoring:
		try:
			live = monitoring[channel][0]
			result = False
			
			#Use a different method depending on Twitch or Hitbox
			if monitoring[channel][1]:
				result = check_twitch(channel)
			else:
				result = check_hitbox(channel)
			
			#If we think about liveness as a clock, we only care about rising and falling edges
			#so we must continue monitoring even after the channel goes live
			
			#If the channel was not live before and is live now,
			#change the status in the dictionary and alert user
			if live is Status.offline and result:
				monitoring[channel] = (Status.online, monitoring[channel][1])
				xchat.command("say " + channel + " is now live on " + ("Twitch at http://www.twitch.tv/" if monitoring[channel][1] else "Hitbox at http://www.hitbox.tv/") + channel)
			#If the channel was live before and is not now,
			#change the status in the dictionary and also alert user
			elif live is Status.online and not result:
				monitoring[channel] = (Status.ending, monitoring[channel][1])
				#Add a deadzone where the stream is dying to handle small disconnects
				timer = xchat.hook_timer(1800000, timer_cb, channel)
				xchat.prnt(channel + " is no longer live")
				if channel == "monotonetim":
					lastStreamTime = time.time()
					file = open(filename, "w")
					file.write(str(lastStreamTime))
					file.close()
			#If the channel was ending but came back within half an hour,
			#set status back to online and don't alert channel
			elif live is Status.ending and result:
				monitoring[channel] = (Status.online, monitoring[channel][1])
				xchat.prnt("Channel came back online soon after disconnecting")
		except urllib2.URLError:
			xchat.prnt("Error checking stream status. Connection likely timed out")
		except:
			xchat.prnt("Unknown error occurred. Error message is " + str(sys.exc_info()))
	return 1

def timer_cb(channel):
	global monitoring
	#Only go offline if the stream didn't come back within this half hour
	if monitoring[channel][0] is Status.ending:
		monitoring[channel] = (Status.offline, monitoring[channel][1])
	return 0

def since_cb(word, word_eol, userdata):
	global lastStreamTime
	global filename
	global cooldown
	global monitoring
	
	if cooldown:
		return xchat.EAT_NONE
	
	command = word[1].split(' ')[0].lower()
	if command == "!since":
		#Command not particularly useful if stream is live
		if monitoring["monotonetim"][0] is Status.online:
			xchat.command("say MonotoneTim is live right now!")
			timer = xchat.hook_timer(60000, cooldown_cb)
			cooldown = True
			return xchat.EAT_NONE
		
		if lastStreamTime == -1:
			file = open(filename, "r")
			lastStreamTime = float(file.read())
			file.close()
		delta = TimeDelta(time.time() - lastStreamTime)
		xchat.command("say " + delta.readableTime())
		timer = xchat.hook_timer(60000, cooldown_cb)
		cooldown = True
	return xchat.EAT_NONE

def cooldown_cb(userdata):
	global cooldown
	#There should only be one cooldown in this script,
	#as the other script covers cooldown commands
	cooldown = False
	return 0
	
xchat.hook_print("Channel Message", since_cb)
xchat.hook_command("monitor", monitor_cb, help = "/MONITOR Alerts when Tim is live")
xchat.hook_command("unmonitor", unmonitor_cb, help = "/UNMONITOR Stop monitoring")
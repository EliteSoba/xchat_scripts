__module_name__ = "Generic bot"
__module_version__ = "0.7"
__module_description__ = "A bot that can add and remove commands"

import xchat
import sqlite3
from passes import passwords
import urllib
import urllib2

#commands: command text, isText integer, output text, cooldown integer
conn = sqlite3.connect('commands.db')
updated = False
commands_url = ""
ran_commands = []
global_commands = ["!add", "!setcooldown", "!delete", "!commands", "!sellout", "!since"]

def check_mod(name):
	if len(name) <3:
		return False
	if name[2] != "@":
		return False
	return True

def showcommands_cb(word, word_eol, userdata):
	global conn
	global global_commands
	global updated
	global commands_url
	
	if updated:
		xchat.command('say ' + commands_url)
	else:
		private = '1'
		name = "Commands"
		expire = 'N'
		format = 'text'
		dev_key = passwords.dev_key
		user_key = passwords.user_key
		url = "http://pastebin.com/api/api_post.php"
		
		#Fetch Commands
		c = conn.cursor()
		c.execute('SELECT command FROM commands')
		code = ""
		for i in c.fetchall():
			code += i[0]
			code += "\n"
		
		#Hardcoded commands
		code += "!commands\n!sellout"
		
		#Delete previous paste
		delete_values = {"api_option" : "delete", "api_user_key" : user_key, "api_dev_key" : dev_key, "api_paste_key" : commands_url.split("/")[-1]}
		
		data = urllib.urlencode(delete_values)
		req = urllib2.Request(url, data)
		response = urllib2.urlopen(req)
		
		if "Paste Removed" != response.read():
			xchat.command('say Warning: Error deleting previous paste')
		
		#Create new paste
		paste_values = {"api_option" : "paste", "api_user_key" : user_key, "api_paste_private" : private, "api_paste_name" : name, "api_paste_expire_date" : expire, "api_paste_format" : format, "api_dev_key" : dev_key, "api_paste_code" : code}
		
		data = urllib.urlencode(paste_values)
		req = urllib2.Request(url, data)
		response = urllib2.urlopen(req)
		
		response = response.read()
		updated = True
		if "Bad API request" in response:
			xchat.command('say Error: Could not create new paste')
		else:
			commands_url = response
			xchat.command('say ' + commands_url)
	
	return xchat.EAT_NONE

def addcommand_cb(word, word_eol, userdata):
	global conn
	global global_commands
	global updated
	
	mod = check_mod(word)
	if not mod:
		return xchat.EAT_NONE
	
	words = word[1].split(' ')
	#Will always have at least one element of words
	if words[0].lower() == "!add":
		if words[1].lower() in global_commands:
			return xchat.EAT_NONE
		
		command = (words[1].lower(),)
		full_command = (words[1].lower(), 0, ' '.join(words[2:]), 60000)
		
		c = conn.cursor()
		c.execute('DELETE FROM commands WHERE command=?', command)
		c.execute('INSERT INTO commands VALUES (?, ?, ?, ?)', full_command)
		xchat.command('say command ' + command[0] + ' successfully added')
		updated = False
		conn.commit()
	
	return xchat.EAT_NONE
	
def setcooldown_cb(word, word_eol, userdata):
	global conn
	global global_commands
	
	mod = check_mod(word)
	if not mod:
		return xchat.EAT_NONE
	
	words = word[1].split(' ')
	#Will always have at least one element of words
	if words[0].lower() == "!setcooldown":
		if words[1].lower() in global_commands:
			return xchat.EAT_NONE
		
		command = words[1].lower()
		try:
			cooldown = int(words[2])
		
			update = (cooldown, command)

			c = conn.cursor()
			c.execute('UPDATE commands SET cooldown=? WHERE command=?', update)
			xchat.command('say Cooldown change for ' + command + ' successful')
			conn.commit()
		except:
			xchat.prnt("Unexpected error:" + sys.exc_info()[0])
			return xchat.EAT_NONE
	
	return xchat.EAT_NONE

def runcommand_cb(word, word_eol, userdata):
	global conn
	global ran_commands
	global global_commands
	
	words = word[1].split(' ')
	command = words[0].lower()
	
	if command in ran_commands or command in global_commands:
		return xchat.EAT_NONE

	safe_command = (command,)
	c = conn.cursor()
	c.execute('SELECT * FROM commands WHERE command=?', safe_command)
	
	result = c.fetchone()
	if result is None:
		return xchat.EAT_NONE
		
	ran_commands += [command]
	
	#Normal text
	if result[1] == 0:
		xchat.command('say ' + result[2])
		timer = xchat.hook_timer(result[3], timer_cb, command)
		return xchat.EAT_ALL
	
	#Special command
	elif result[1] == 1:
		return xchat.EAT_NONE
	
	return xchat.EAT_NONE
	
def deletecommand_cb(word, word_eol, userdata):
	global conn
	global global_commands
	global updated
	
	mod = check_mod(word)
	if not mod:
		return xchat.EAT_NONE
	
	words = word[1].split(' ')
	#Will always have at least one element of words
	if words[0].lower() == "!delete":
		if words[1].lower() in global_commands:
			return xchat.EAT_NONE
		
		command = (words[1].lower(),)
		
		c = conn.cursor()
		c.execute('DELETE FROM commands WHERE command=?', command)
		xchat.command('say command ' + words[1].lower() + ' deleted')
		updated = False
		conn.commit()
	
	return xchat.EAT_NONE
	
	
def timer_cb(userdata):
	global ran_commands
	ran_commands.remove(userdata)
	return 0

	
def mastercommand_cb(word, word_eol, userdata):
	global conn
	global ran_commands
	global global_commands
	
	command = word[1].split(' ')[0].lower()

	if command in global_commands:
		if command == "!add":
			addcommand_cb(word, word_eol, userdata)
		elif command == "!setcooldown":
			setcooldown_cb(word, word_eol, userdata)
		elif command == "!delete":
			deletecommand_cb(word, word_eol, userdata)
		elif command == '!commands':
			showcommands_cb(word, word_eol, userdata)
	else:
		runcommand_cb(word, word_eol, userdata)
	
	return xchat.EAT_NONE
	
	
xchat.hook_print("Channel Message", mastercommand_cb)

__module_name__ = "Generic bot"
__module_version__ = "0.5"
__module_description__ = "A bot that can add and remove commands"

import xchat
import sqlite3

#commands: command text, isText integer, output text, cooldown integer
conn = sqlite3.connect('commands.db')
ran_commands = []
global_commands = ["!add", "!setcooldown", "!delete"]

def check_mod(name):
	if len(name) <3:
		return False
	if name[2] != "@":
		return False
	return True


def addcommand_cb(word, word_eol, userdata):
	global conn
	global global_commands
	
	mod = check_mod(word)
	if not mod:
		return xchat.EAT_NONE
	
	words = word[1].split(' ')
	#Will always have at least one element of words
	if words[0].lower() == "!add":
		if words[1].lower() in global_commands:
			return xchat.EAT_NONE
		
		if words[1][0] != "!":
			return xchat.EAT_NONE
		
		command = (words[1].lower(),)
		full_command = (words[1].lower(), 0, ' '.join(words[2:]), 60000)
		
		c = conn.cursor()
		c.execute('DELETE FROM commands WHERE command=?', command)
		c.execute('INSERT INTO commands VALUES (?, ?, ?, ?)', full_command)
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
			update = (command, cooldown)
			
			c.execute('UPDATE commands SET cooldown=? WHERE command=?', update)
			
			c = conn.cursor()
			conn.commit()
		except:
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
	xchat.prnt("penis" + command)
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
	if command[0] != "!":
		return xchat.EAT_NONE
	
	if command in global_commands:
		if command == "!add":
			addcommand_cb(word, word_eol, userdata)
		elif command == "!setcooldown":
			setcooldown_cb(word, word_eol, userdata)
		elif command == "delete":
			deletecommand_cb(word, word_eol, userdata)
	else:
		runcommand_cb(word, word_eol, userdata)
	
	return xchat.EAT_NONE
	
	
xchat.hook_print("Channel Message", mastercommand_cb)

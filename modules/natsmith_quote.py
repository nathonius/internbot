import willie
import os.path
import time

def setup(bot):
	if bot.db:
		columns = ['victim', 'quote', 'time']
		if not getattr(bot.db, 'nquote'):
			bot.db.add_table('nquote', columns, 'victim')

def get_victim(trigger):
	msg = trigger.bytes.split()
	victim = msg[1]
	return victim

def get_quote(table, victim):
	(quote, time) = table.get(victim, ('quote', 'time'), 'victim')
	return (quote, time)

def get_quote_string(trigger):
	msg = trigger.bytes.split()
	quote_string = " ".join(msg[2:])
	quote_string = quote_string.strip('\"\'')
	return quote_string

def check_victim(line, victim):
	victim_pos = str(line).find(':')+1
	end_pos = str(line).find('!')
	found_victim = str(line)[victim_pos:end_pos]
	return (str(victim) == str(found_victim))

def escape(quote):
	newquote = quote.replace("'", "''")
	return newquote

def unescape(quote):
	newquote = quote.replace("''", "'")
	return newquote

def parse_quote(line, victim):
	time_str = line.split()[0]
	time_str = float(time_str[2:])
	time_obj = time.localtime(time_str)
	format_str = '[%Y-%m-%d %H:%M:%S]'#[yyyy-mm-dd hh:mm:ss]
	time_str = time.strftime(format_str, time_obj)

	privmsg_pos = line.find('PRIVMSG')
	line = line[privmsg_pos:]
	msg_pos = line.find(':')+1
	quote = line[msg_pos:]

	return(quote, time_str)

def find_quote(victim, quote_string):
	script_dir = os.path.dirname(__file__)
	willie_dir = os.path.dirname(script_dir)
	log_path = os.path.join(willie_dir, "logs/raw.log")
	log = open(log_path, 'r')
	possible_lines = []
	for line in log:
		if('PRIVMSG' in str(line) and str(victim) in str(line) and 'addquote' not in str(line) and check_victim(str(line), victim)):
			possible_lines.append(str(line))
	possible = len(possible_lines)-1
	if(str(quote_string) == ""):
		(quote, time) = parse_quote(possible_lines[-1], victim)
		return (quote, time)
	for i in range(possible, -1, -1):
		if(str(quote_string).lower() in str(possible_lines[i]).lower()):
			(quote, time) = parse_quote(possible_lines[i], victim)
			return (quote, time)
	return ('QUOTENOTFOUND', '0')


@willie.module.rule(r'^addquote')
def add_quote(bot, trigger):
	table = bot.db.nquote
	try:
		victim = get_victim(trigger)
	except:
		return
	quote_string = get_quote_string(trigger)
	try:
		(quote, time) = find_quote(victim, quote_string)
		quote = escape(quote)
	except:
		quote = 'QUOTENOTFOUND'
	if(quote == 'QUOTENOTFOUND'):
		bot.say(victim+' did not say "'+quote_string+'".')
	else:
		columns = {'quote':str(quote), 'time':str(time), 'victim':str(victim)}
		#bot.say('quote: '+str(quote)+', time: '+str(time)+', victim: '+str(victim))
		table.update(victim, columns)
		quote = unescape(quote)
		bot.say('Remembered quote "'+quote+'" -- '+victim)



@willie.module.rule(r'^quote')
def quote(bot, trigger):
	table = bot.db.nquote
	try:
		victim = get_victim(trigger)
	except:
		return
	try:
		(quote, time) = get_quote(table, victim)
	except:
		quote = None
	if(quote == None):
		bot.say('No quote found for '+victim+'.')
	else:
		bot.say('"'+quote+'" -- '+victim+' '+time)
import willie
import time

def setup(bot):
	if bot.db:
		columns = ['victim', 'karma','last']
		if not getattr(bot.db, 'nkarma'):
			bot.db.add_table('nkarma', columns, 'victim')

def get_victim(trigger, amount):
	"""Returns the person whose karma is being changed"""
	string = trigger.bytes
	if(amount == 1):
		victim = string[:string.find('++')]
	else:
		victim = string[:string.find('--')]
	victim = victim.split()[-1]
	return victim

def get_last(table, triggerUser):
	last_time = table.get(triggerUser, ('last'), 'victim')
	return last_time

def get_karma(table, victim):
	karma = table.get(victim, ('karma'), 'victim')
	return karma

def update_karma(bot, trigger, amount):
	"""Main function"""
	table = bot.db.nkarma
	victim = get_victim(trigger, amount)
	triggerUser = trigger.nick
	try:
		last = int(get_last(table, triggerUser))
	except:
		last = 0
	#prevent flooding
	if((time.time() - int(last)) < 5):
		pass
	else:
		#if the person calling it is also the victim, we decrease their karma
		if(victim == triggerUser):
			amount = -1
		if(victim == 'intern' or victim == 'intern2'):
			amount = 1
		try:
			karma = int(get_karma(table, victim))
		except:
			karma = 0
		karma += amount
		columns = {'karma':str(karma)}
		#update the karma
		table.update(victim, columns)
		columns = {'last':str(time.time())}
		#update the last variable
		table.update(triggerUser, columns)
		bot.say(victim+' now has '+str(karma)+' point(s) of karma')

@willie.module.rule(r'^.*[\w][\S]+(\+\+)')
def increase_karma(bot, trigger):
	update_karma(bot, trigger, 1)

@willie.module.rule(r'^.*[\w][\S]+(\-\-)')
def decrease_karma(bot, trigger):
	update_karma(bot, trigger, -1)

@willie.module.rule(r'^rank+[\s]*[\w][\S]+')
def report_karma(bot, trigger):
	table = bot.db.nkarma
	victim = trigger.bytes.split()[-1]
	try:
		karma = get_karma(table, victim)
	except:
		karma = 0
	if(karma == None):
		karma = 0
	bot.say(victim+' has '+str(karma)+' point(s) of karma')



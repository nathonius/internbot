from willie import module

@module.rule(r'.*(?i)good morning')
def maverick(bot, trigger):
	"""says good morning, but only to maverick or natsmith"""
	if(trigger.nick == 'maverick' or trigger.nick == 'natsmith'):
		bot.say('Good morning, ' + trigger.nick)
		bot.say('https://www.youtube.com/watch?v=s1I7D5MsSvU')
	else
		bot.say('https://www.youtube.com/watch?v=s1I7D5MsSvU')

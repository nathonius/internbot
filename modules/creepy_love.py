from willie import module

@module.rule(r'^(?i)(i love you)+[,]*[\s]')
def creepy_love(bot, trigger):
	"""when someone says i love you <nick> or i love you, <nick>, willie says i love you more than <trigger>, <nick>"""
	#words [0, 1, 2] are the words 'i', 'love', and 'you'
	words = trigger.bytes.split()
	if(len(words) <= 4):
		victim = words[3]
		bot.say('I love you more than '+str(trigger.nick)+', '+victim)
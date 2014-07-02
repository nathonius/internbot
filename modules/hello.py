from willie import module

@module.rule(r'^[hello]+[\W]*[\s]+[intern]')
def hi(bot, trigger):
    bot.say('Hi, ' + trigger.nick)
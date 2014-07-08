from willie import module

@module.rule(r'.*(?i)(party)')
def party(bot, trigger):
  """when someone says party, internbot dances"""
  bot.say(':D\-<')
  bot.say(':D|-<')
  bot.say(':D/-<')

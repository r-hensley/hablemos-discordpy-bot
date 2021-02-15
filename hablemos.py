import os
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv('.env')


bot = commands.Bot(command_prefix="!", help_command=None)

# for when the bot gets bigger:
# for filename in os.listdir("./cogs"):
#     if filename.endswith(".py") and filename != "__init__.py" and filename != "__init__.py":
#         bot.load_extension(f'cogs.{filename[:-3]}')

bot.load_extension('cogs.convo_starter')
bot.load_extension('cogs.general')

bot.run(os.getenv('BOT_TOKEN'))

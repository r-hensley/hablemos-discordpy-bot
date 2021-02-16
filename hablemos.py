import os
from discord import Game
from discord.ext.commands import Bot
from dotenv import load_dotenv

load_dotenv('.env')

PREFIX = "!"
cog_extensions = ['cogs.convo_starter', 'cogs.general']


# for when the bot gets bigger:
# for filename in os.listdir("./cogs"):
#     if filename.endswith(".py") and filename != "__init__.py" and filename != "__init__.py":
#         bot.load_extension(f'cogs.{filename[:-3]}')


class Hablemos(Bot):

    def __init__(self):
        super().__init__(description="Bot by Jaleel#6408", command_prefix=PREFIX, owner_id=216848576549093376,
                         help_command=None)

        for extension in cog_extensions:
            self.load_extension(extension)
            print(f"{extension} loaded")

    async def on_ready(self):
        print("BOT LOADED!")
        await self.change_presence(activity=Game(f'{PREFIX}help for help'))


bot = Hablemos()
bot.run(os.getenv('BOT_TOKEN'))

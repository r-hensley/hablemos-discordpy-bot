import os
from discord import Game, Client
from discord.ext.commands import Bot, CommandNotFound, Cog
from dotenv import load_dotenv

load_dotenv('.env')

PREFIX = "$"
cog_extensions = ['cogs.convo_starter', 'cogs.general']
client = Client()

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

    async def on_command_error(self, ctx, error):
        ignored = (CommandNotFound,)

        if isinstance(error, ignored):
            guild = client.get_guild(523754549953953793)
            print(type(guild))
            # await channel.send("Test")


bot = Hablemos()
bot.run(os.getenv('BOT_TOKEN'))

from os import getenv
from discord import Game, Intents
from discord.ext.commands import Bot, CommandNotFound, CommandOnCooldown
from dotenv import load_dotenv
from cogs.general import PREFIX_

load_dotenv('.env')

PREFIX = PREFIX_
cog_extensions = ['cogs.convo_starter',
                  'cogs.general',
                  'cogs.hangman_controller',
                  'cogs.quote_generator',
                  'cogs.pages']


class Hablemos(Bot):
    error_channel = ""
    online_channel = ""

    def __init__(self):
        super().__init__(description="Bot by Jaleel#6408",
                         command_prefix=PREFIX,
                         owner_id=216848576549093376,
                         help_command=None,
                         intents=Intents(members=True, messages=True, guilds=True)
                         )

        for extension in cog_extensions:
            self.load_extension(extension)
            print(f"{extension} loaded")

    async def on_ready(self):
        # error log in my personal server
        self.error_channel = self.get_guild(731403448502845501).get_channel(811669166883995690)
        self.online_channel = self.get_guild(731403448502845501).get_channel(808679873837137940)

        print("BOT LOADED!")
        await self.online_channel.send("I'm online bra :smiling_imp:")
        await self.change_presence(activity=Game(f'{PREFIX}topic for a conversation starter'))

    async def on_command_error(self, ctx, error):
        if ctx.message.content[1].isdigit() or ctx.message.content[-1] == PREFIX:  # ignores dollar amounts and math bot
            return
        if isinstance(error, CommandNotFound):
            await self.error_channel.send(
                f"------\nCommand not found:\n{ctx.author}, {ctx.author.id}, {ctx.channel}, {ctx.channel.id}, {ctx.guild}, {ctx.guild.id}, \n{ctx.message.content}\n{ctx.message.jump_url}\n------")

        if isinstance(error, CommandOnCooldown):
            await ctx.send(f"This command is on cooldown.  Try again in {round(error.retry_after)} seconds.")

    async def on_command_completion(self, ctx):
        await self.error_channel.send(
            f"------\nSuccesfully used by {ctx.author}, {ctx.channel},{ctx.guild}, {ctx.message.content}\n{ctx.message.jump_url}\n------")


bot = Hablemos()
bot.run(getenv('BOT_TOKEN'))

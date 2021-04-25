import os
from discord import Game, Embed, Color
from discord.ext.commands import Bot, CommandNotFound, Cog
from dotenv import load_dotenv

load_dotenv('.env')

PREFIX = "$"
cog_extensions = ['cogs.convo_starter', 'cogs.general', 'cogs.other']


class Hablemos(Bot):

    def __init__(self):
        super().__init__(description="Bot by Jaleel#6408", command_prefix=PREFIX, owner_id=216848576549093376,
                         help_command=None)

        for extension in cog_extensions:
            self.load_extension(extension)
            print(f"{extension} loaded")

    async def on_ready(self):
        # error log in my personal server
        self.error_channel = self.get_guild(523754549953953793).get_channel(811845363890913300)

        print("BOT LOADED!")
        await self.change_presence(activity=Game(f'{PREFIX}topic for a conversation starter'))

    async def on_command_error(self, ctx, error):
        ignored = (CommandNotFound,)

        if isinstance(error, ignored):
            await self.error_channel.send(f"------\nCommand not found:\n{ctx.author}, {ctx.author.id}, {ctx.channel}, {ctx.channel.id}, {ctx.guild}, {ctx.guild.id}, \n{ctx.message.content}\n{ctx.message.jump_url}\n------")

    async def on_command_completion(self, ctx):
        await self.error_channel.send(
            f"------\nSuccesfully used by {ctx.author}, {ctx.channel},{ctx.guild}, {ctx.message.content}\n{ctx.message.jump_url}\n------")


bot = Hablemos()
bot.run(os.getenv('BOT_TOKEN'))

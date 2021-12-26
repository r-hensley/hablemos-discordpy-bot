from discord.ext.commands import Cog


class BaseCog(Cog):
    """Base class for all cogs"""
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def cog_command_error(ctx, error):
        print(f'An error occurred: {error} in {ctx.channel}')

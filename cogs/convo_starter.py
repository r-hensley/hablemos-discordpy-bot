from discord.ext import commands


class ConvoStarter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # embed = Embed(description=f'Suggest more topics [here]({SUGGESTION_FORM})!', color=Color.blurple())
    # @commands.command()
    # async def topic


def setup(bot):
    bot.add_cog(ConvoStarter(bot))

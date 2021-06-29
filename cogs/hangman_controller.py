from discord.ext import commands
from cogs.utils.hangman_data.hangman import Hangman


class HangmanController(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game_in_progress = False
        self.channels = []

    @commands.command(aliases=['hm', 'hang',])
    async def hangman(self, ctx):
        """
        (still experimental, please let me know of any errors)
        Hangman but in Spanish. I currently only have `animales` as a category.
        Some or most of the vocabulary might be very Spanish (from :flag_es:).
        Ping or dm <@216848576549093376> if you have any suggestions.

        Type `$hangman` to start a new game
        Type `quit` to exit the game, only the person who started can quit the game.
        The game will automatically exit after 45 seconds if there's no input
        """
        channel = ctx.channel.id
        await self.new_game(ctx, channel)

    async def new_game(self, context, channel):
        if self.game_in_progress and channel in self.channels:
            return await context.send("There's already a game in progress in this channel")
        self.channels.append(channel)
        self.game_in_progress = True
        new_game = Hangman(self.bot)
        await new_game.hangman(context)
        self.channels.remove(channel)


def setup(bot):
    bot.add_cog(HangmanController(bot))

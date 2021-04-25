# Where I test other non-important commands

from random import choice
from .convo_starter import colors
from .general import General as gen
from discord.ext import commands
from discord import Embed
import os

dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def embed_quote(quote):
    embed = Embed(color=choice(colors))
    embed.clear_fields()
    embed.title = quote
    embed.set_footer(text="Cardi B")
    return embed


class Other(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def get_quote(self):
        with open(f"{dir_path}/cogs/utils/data.txt", 'r', encoding='utf 8') as quotes:
            lines = quotes.read().splitlines()
            cita = choice(lines)

        return cita

    @commands.command()
    async def cardi(self, ctx):
        emb = embed_quote(self.get_quote())

        await gen.safe_send(ctx.channel, ctx, embed=emb)


def setup(bot):
    bot.add_cog(Other(bot))

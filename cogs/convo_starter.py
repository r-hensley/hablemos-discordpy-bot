from discord.ext import commands
from discord import Embed, Color

try:
    from convo_db import random_question
except ImportError:
    from .convo_db import random_question

columns = ['generales', 'personales', 'televisión', 'películas', 'libros', 'música',
           'móviles', 'aplicaciones', 'deportes', 'restaurantes', 'viajes', 'tecnología', 'ropa',
           'metas', 'temporadas', 'feriados', 'educación', 'comida_cocina', 'extrañas']


class ConvoStarter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['topic', 'top', 'rand'])
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def general(self, ctx):
        embed = Embed(description=f"Suggest more topics [here]({'www.google.com'})!", color=Color.blurple())
        embed.title = random_question(columns[0])
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ConvoStarter(bot))

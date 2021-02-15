from random import choice
from .convo_db import random_question
from discord.ext import commands
from discord import Embed, Color



# Embed Message
DEEPL_URL = "https://www.deepl.com/translator"
SUGGESTION_FORM = "https://docs.google.com/forms/d/1yDMkL0NLlPWWuNy2veMr3PLoNjYc2LTD_pnqYurP91c/"
FOOTER_ENG = f"Questions translated using [DeepL]({DEEPL_URL}). Feel free to use [this link]({SUGGESTION_FORM}) " \
             f"to report a mistake or suggest a question"
FOOTER_ESP = f"\nPreguntas traducidas con [DeepL]({DEEPL_URL}). Utiliza [este enlace]({SUGGESTION_FORM}) " \
             f"para reportar un error o sugerir una pregunta"
ERROR_MESSAGE = "The proper format is ``!topic <topic>`` eg. ``!topic movies``. Please see " \
                "``!help topic`` for more info"

NOT_FOUND = "Topic not found! Please type ``!lst`` to see a list of topics"

# Spa and Eng Channel IDs
spa_channels = [809349064029241344, ]
# eng_channels = [809349081657901126, ]

# Names of the sqlite tables, in order
tables = {'general': 'generales', 'personal': 'personales', 'tv': 'televisión', 'movies': 'películas',
          'books': 'libros', "music": 'música',
          'tech': 'tech', 'sport': 'deportes', 'food': 'comida_cocina', 'travel': 'viajes', 'fashion': 'ropa',
          'holidays': 'temporadas', 'education': 'educación', 'strange': 'extrañas', 'philo': 'filo'}

tables_keys = list(tables.keys())
tables_values = list(tables.values())


# Embed question

def embed_question(question_1a, question_1b):
    embed = Embed(color=Color.blurple())
    embed.clear_fields()
    embed.title = question_1a
    embed.description = f"**{question_1b}**"
    embed.add_field(name="\u200b", value=FOOTER_ESP, inline=False)
    return embed


class ConvoStarter(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['top',])
    async def topic(self, ctx, *category):
        """
        Command used to suggestion a random conversation topic. Type `!topic <category>`. Just typing `!topic` will suggest a topic from the `general` category.

        Type `;lst` to see the list of categories.

        Example: `!topic food`"""

        table = ""
        if len(category) > 1:
            await ctx.send(ERROR_MESSAGE)
            return
        elif len(category) == 0:
            table = "generales"
        else:
            if category[0] in tables_keys:
                table = tables[category[0]]
            elif category[0] == 'rand' or category[0] == 'random':
                table = choice(tables_values)
            else:
                await ctx.send(NOT_FOUND)
                return

        question_spa_eng = random_question(table)
        if ctx.channel.id == spa_channels[0]:
            emb = embed_question(question_spa_eng[0], question_spa_eng[1])
            await ctx.send(embed=emb)
        else:
            emb = embed_question(question_spa_eng[1], question_spa_eng[0])
            await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(ConvoStarter(bot))

# @commands.bot_has_permissions(send_messages=True, embed_links=True)

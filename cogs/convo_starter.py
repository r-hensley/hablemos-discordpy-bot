from random import choice
from cogs.utils.convo_starter_data.convo_starter_help import categories, get_random_question
from cogs.general import safe_send
from discord.ext import commands
from discord import Embed


# Embed Message
DEEPL_URL = "https://www.deepl.com/translator"
# SUGGESTION_FORM = "https://docs.google.com/forms/d/1yDMkL0NLlPWWuNy2veMr3PLoNjYc2LTD_pnqYurP91c/"
# FOOTER_ENG = f"Questions translated using [DeepL]({DEEPL_URL}). Feel free to use [this link]({SUGGESTION_FORM}) " \
#              f"to report a mistake or suggest a question"
# FOOTER_ESP = f"\nPreguntas traducidas con [DeepL]({DEEPL_URL}). Utiliza [este enlace]({SUGGESTION_FORM}) " \
#              f"para reportar un error o sugerir una pregunta"
ERROR_MESSAGE = "The proper format is `$topic <topic>` eg. `$topic movies`. Please see " \
                "`$help topic` for more info"

NOT_FOUND = "Topic not found! Please type ``$lst`` to see a list of topics"

# Spa and Eng Channel IDs
spa_channels = [809349064029241344, 243858509123289089, 388539967053496322, 477630693292113932]
#  personal server, spa-eng, spa-eng, esp-ing
# eng_channels = []

# Embed question
colors = [0x7289da, 0xe74c3c, 0xe67e22, 0xf1c40f, 0xe91e63, 0x9b59b6,
          0x3498db, 0x2ecc71, 0x1abc9c]


def embed_question(question_1a, question_1b):
    embed = Embed(color=choice(colors))
    embed.clear_fields()
    embed.title = question_1a
    embed.description = f"**{question_1b}**"
    # embed.add_field(name="\u200b", value=footer, inline=False)
    return embed


class ConvoStarter(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['top', ])
    async def topic(self, ctx, *category):
        """
        Command used to suggestion a random conversation topic. Type `$topic <category>`. Just typing `$topic` will suggest a topic from the `general` category.

        Type `$lst` to see the list of categories.

        Examples: `$topic`, `$topic phil`, `$topic 4`"""

        table = ""
        if len(category) > 1:
            await ctx.send(ERROR_MESSAGE)
            return
        elif len(category) == 0:
            table = "general"
        elif category[0] in categories:
            table = category[0]
        elif category[0] in ['1', '2', '3', '4']:
            table = categories[int(category[0]) - 1]
        else:
            await ctx.send(NOT_FOUND)
            return

        question_spa_eng = get_random_question(table)

        if ctx.channel.id in spa_channels:
            emb = embed_question(question_spa_eng[0], question_spa_eng[1])
        else:
            emb = embed_question(question_spa_eng[1], question_spa_eng[0])
        await safe_send(ctx, embed=emb)


def setup(bot):
    bot.add_cog(ConvoStarter(bot))

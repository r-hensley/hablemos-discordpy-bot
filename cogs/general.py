from discord.ext import commands
from discord import Embed, Color, Forbidden

SOURCE_URL = 'https://github.com/Jaleel-VS/hablemos-discordpy-bot#sources'
REPO = 'https://github.com/Jaleel-VS/hablemos-discordpy-bot'
DPY = 'https://discordpy.readthedocs.io/en/latest/'


def green_embed(text):
    return Embed(description=text, color=Color(int('00ff00', 16)))


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def safe_send(self, destination, content=None, *, embed=None):
        try:
            return await destination.send(content, embed=embed)
        except Forbidden:
            print(f"I don't have permission to send messages in:\nChannel: #{destination.channel.name}"
                  f"\nGuild: {destination.guild.id}")

    @commands.command()
    async def help(self, ctx, arg=''):
        if arg:
            requested = self.bot.get_command(arg)
            if not requested:
                await self.safe_send(ctx, "I was unable to find the command you requested")
                return
            message = ""
            message += f"**;{requested.qualified_name}**\n"
            if requested.aliases:
                message += f"Aliases: `{'`, `'.join(requested.aliases)}`\n"
            if requested.help:
                message += requested.help
            emb = green_embed(message)
            await self.safe_send(ctx, embed=emb)
        else:
            to_send = """
            Type `$help <command>` for more info on any command or category.
            
            __**General**__: 
                `info` - Display information and a GitHub link to the source code
            __**Conversation starters**__: 
                `topic` - Displays random conversation starter 
                `lst` - Lists available categories
            """
            await self.safe_send(ctx, embed=green_embed(to_send))

    @commands.command(aliases=['list', ])
    async def lst(self, ctx):
        """
        Lists available categories
        """
        categories = f"""    
        To use any one of the undermentioned topics type `$topic <category>`. 
        `$topic` or `$top` defaults to `general`
        
        command(category) - description:
        `general` - General questions
        `personal` - Personal questions
        `open` - Open-ended questions
        `strange` - Strange/weird questions
        `phil` - Philosophical questions
        
        `games` - Questions related to games
        `tv` - Questions about series/anime/cartoons
        `books` - Questions related to books
        `music` - Questions related to music
        `tech` - Questions about technology
        `sport` - Questions related to sports
        `food` - Questions related to food
        `lang`- Questions related to language learning
        `fashion` - Questions related to fashion and clothes
        `holi` - Questions related to holidays and seasons
        `movies` - Questions related to movies
        `travel` - Questions related to travel
        `edu` - Questions about education
                
        `random`, `rand` - A random question from any of the above categories

        [Source]({SOURCE_URL})        
        """
        await self.safe_send(ctx, embed=green_embed(categories))

    @commands.command()
    async def info(self, ctx):
        """
        Information about the bot
        """

        text = f"""
        The bot was coded in Python using the [discord.py]({DPY}) API and SQLite3 as the database.
        
        To report an error or make a suggestion please message <@216848576549093376>
        [Github Repository]({REPO})
        """

        await self.safe_send(ctx, embed=green_embed(text))

    @commands.command()
    async def ping(self, ctx):
        await self.safe_send(ctx,
                             embed=green_embed(f"**Command processing time**: {round(self.bot.latency * 1000, 2)}ms"))


def setup(bot):
    bot.add_cog(General(bot))

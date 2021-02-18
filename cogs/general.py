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
        **There are 18 categories**
        
        To use any one of them type `$topic <category>`. `$topic` defaults to `general`
        
        command - description (number of questions):
        `general` - General questions (140)
        `personal` - Personal questions (125)
        `open` - Open-ended questions (100)
        `strange` - Strange/weird questions (183)
        `phil` - Philosiphical questions (202)
        
        `games` - Questions related to games (50)
        `tv` - Questions about series/anime/cartoons (18)
        `books` - Questions relating to books (16)
        `music` - Questions related to music (14)
        `tech` - Questions about technology (33)
        `sport` - Questions related to sports (12)
        `food` - Questions related to food (23)
        `lang`- Questions related to language learning (10)
        `fashion` - Questions related to fashion and clothes (12)
        `holi` - Questions related to holidays and seasons (20)
        `movies` - Questions related to movies (13)
        `travel` - Questions related to travel (19)
        `edu` - Questions about education (11) 
                
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
        The bot was coded in Python using the [discord.py API]({DPY}) and SQLite3 as the database.
        
        [Github Repository]({REPO})
        """

        await self.safe_send(ctx, embed=green_embed(text))

    @commands.command()
    async def ping(self, ctx):
        await self.safe_send(ctx,
                             embed=green_embed(f"**Command processing time**: {round(self.bot.latency * 1000, 2)}ms"))


def setup(bot):
    bot.add_cog(General(bot))

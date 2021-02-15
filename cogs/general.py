from discord.ext import commands
from discord import Embed, Color

SOURCE_URL = 'https://mundodepreguntas.com/preguntas'


def green_embed(text):
    return Embed(description=text, color=Color(int('00ff00', 16)))


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, arg=''):
        if arg:
            requested = self.bot.get_command(arg)
            if not requested:
                await ctx.send("I was unable to find the command you requested")
                return
            message = ""
            message += f"**;{requested.qualified_name}**\n"
            if requested.aliases:
                message += f"Aliases: `{'`, `'.join(requested.aliases)}`\n"
            if requested.help:
                message += requested.help
            emb = green_embed(message)
            await ctx.send(embed=emb)
        else:
            to_send = "Type `;help <command>` for more info on any command or category. For (subcommands), chain with" \
                      " the parent command.\n\n"
            await ctx.send(to_send)

    @commands.command()
    async def lst(self, ctx):
        """
        Lists available categories
        """
        categories = f"""
        **There are 16 categories**
        
        To use any one of them type `!topic <category>`
        
        command - description (number of questions):
        `general` - General questions (140)
        `personal` - Personal questions (125)
        `open` - Open-ended questions (100)
        `strange` - Strange/weird questions (183)
        `phil` - Philosiphical questions (202)
        
        `books` - Questions relating to books (16)
        `music` - Questions related to music (14)
        `tech` - Questions about technology (33)
        `sport` - Questions related to sports (12)
        `food` - Questions related to food (23)
        `holi` - Questions related to holidays and seasons (20)
        `movies` - Questions related to movies (13)
        `music` - Questions related to musics
        `travel` - Questions related to travel 
        `edu` - Questions about education (11)
                
        `random`, `rand` - A random from any of the above categories
           
        [Source]({SOURCE_URL})        
        """
        await ctx.send(embed=green_embed(categories))


def setup(bot):
    bot.add_cog(General(bot))

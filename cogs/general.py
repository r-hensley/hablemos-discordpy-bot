from discord.ext import commands
from discord import Embed, Color, Forbidden

SOURCE_URL = 'https://docs.google.com/spreadsheets/d/10jsNQsSG9mbLZgDoYIdVrbogVSN7eAKbOfCASA5hN0A/edit?usp=sharing'
REPO = 'https://github.com/Jaleel-VS/hablemos-discordpy-bot'
DPY = 'https://discordpy.readthedocs.io/en/latest/'
PREFIX_ = "$"


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
            message += f"**{PREFIX_}{requested.qualified_name}**\n"
            if requested.aliases:
                message += f"Aliases: `{'`, `'.join(requested.aliases)}`\n"
            if requested.help:
                message += requested.help
            emb = green_embed(message)
            await self.safe_send(ctx, embed=emb)
        else:
            to_send = """
            Type `$help <command>` for more info about on any command.
            
            **General**: 
                `info` - Display information and a GitHub link to the source code
            **Conversation starters**: 
                `topic` - Displays random conversation starter 
                `lst` - Lists available categories
            **Hangman**
                `hangman` - Starts a new game
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
        `general`, `1` - General questions
        `phil`, `2` - Philosophical questions
        `would`, `3` - *'Would you rather'* questions
        `other`, `random`, `4` -  Random questions

        [Full list of questions]({SOURCE_URL})        
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

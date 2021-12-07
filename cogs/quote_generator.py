"""
Fun utility that creates quotes using the message content and username of a user
and converts it to an image using html and css
"""
from re import sub

from cogs.utils.quote_generator_data.image_creator import dir_path

from discord.ext.commands import Cog, command, cooldown, BucketType
from discord import Embed, File
import emoji


from os import remove

from cogs.utils.quote_generator_data.image_creator import create_image


def get_img_url(user_id: int, url_identifier: str):
    if url_identifier is None: # user doesn't have a profile picture
        return "https://i.imgur.com/z9tOsSz.png"
    return f"https://cdn.discordapp.com/avatars/{user_id}/{url_identifier}.png?size=256"


def remove_emoji_from_message(message):
    return sub("<:[A-Za-z0-9_]+:([0-9]+)>", '', message).replace("  ", " ")


def give_emoji_free_text(text):
    return emoji.get_emoji_regexp().sub(r'', text)[:28]


async def get_html_css_info(channel, message_id, server):
    message = await channel.fetch_message(message_id)
    user_id = message.author.id
    user = await server.fetch_member(user_id)
    message_content = remove_emoji_from_message(message.content)
    user_nick = user.display_name if user.nick is None else give_emoji_free_text(user.nick)
    user_avatar = get_img_url(user_id, user.avatar)

    return user_nick, user_avatar, message_content


class QuoteGenerator(Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @command(aliases=['q', ])
    @cooldown(1, 10, type=BucketType.user)
    async def quote(self, ctx, *user_input):
        """
        (still testing, please report any errors or suggestions)
        Generates a dramatically themed quote using a message url, your own message or replying to a message.
        Images and custom emojis won't show up and there's a limit to 150 words.

        Example usage:
        `$quote https://discord.com/channels/731403448502845501/808679873837137940/916938526329798718`
        (creates a quote using a specific message)
        `$quote ¡Viva México, cabrones!`
        (creates a quote using your own message)

        NOTE: The message id doesn't work, only the full link.

        I'll make it a slash command eventually, should be easier to use
        """

        is_message_reply = ctx.message.reference is not None
        if len(user_input) == 0 and not is_message_reply:
            return await ctx.send("Please see type `$help quote` for info on correct usage")

        if len(user_input) == 1 and len(user_input[0]) == 18 and user_input[0].isdigit() and not is_message_reply:
            return await ctx.send(
                "You tried to use a message_id. Please use a link or just a regular message. See `$help quote` for "
                "correct usage")
        user_nick = ""
        user_avatar = ""
        message_content = ""

        if is_message_reply:
            message_id = ctx.message.reference.message_id
            guild_id = ctx.message.reference.guild_id
            channel_id = ctx.message.reference.channel_id
            server = self.bot.get_guild(guild_id)
            channel = server.get_channel(channel_id)

            user_nick, user_avatar, message_content = await get_html_css_info(channel, message_id, server)

        elif len(user_input) == 1 and user_input[0].startswith("https://discord.com/channels/"):
            link = user_input[0].split('/')
            server_id = int(link[4])
            channel_id = int(link[5])
            msg_id = int(link[6])

            server = self.bot.get_guild(server_id)
            if server is None:
                return await ctx.send("I can't access this server")
            channel = server.get_channel(channel_id)
            if channel is None:
                return await ctx.send("I can't access this channel")

            user_nick, user_avatar, message_content = await get_html_css_info(channel, msg_id, server)

        else:
            message_content = remove_emoji_from_message(' '.join(user_input))
            user_nick = ctx.author.display_name if ctx.author.nick is None else give_emoji_free_text(ctx.author.nick)
            user_avatar = get_img_url(ctx.author.id, ctx.author.avatar)

        if len(message_content) > 150:
            return ctx.send("Beep boop, I can't create an image with that much text. I'm limited at 150 characters")
        generated_url = create_image(user_nick, user_avatar, message_content)

        await ctx.send(file=File(generated_url))

        # delete file
        remove(f"{dir_path}/quote_generator_data/picture.png")
        print("File removed")


def setup(bot):
    bot.add_cog(QuoteGenerator(bot))

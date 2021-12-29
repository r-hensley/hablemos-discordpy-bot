from cogs.utils.reverso_data.helper import HelperFunctions
from base_cog import BaseCog

from discord.ext.commands import command, cooldown, BucketType
from discord.ext import pages
from reverso_api.context import ReversoContextAPI as reverso
from discord import Embed, Color, ButtonStyle

helper_functions = HelperFunctions()
NOT_FOUND_ERROR = "Input not recognised. Please type `$langcodes` to see a list of available languages. " \
                  "Please type `$help reverso` for correct usage."

REVERSO_URL = "https://context.reverso.net/translation/"
REPO = "https://discord.com/channels/731403448502845501/808679873837137940"


class Reverso(BaseCog):
    languages = None
    user_input = None

    def __init__(self, bot):
        super().__init__(bot)

    @command(aliases=['rev', 'reverse', ])
    @cooldown(1, 10, type=BucketType.user)
    async def reverso(self, ctx, lang_original=None, lang_target=None, *, message=None) -> None:
        """
        (still experimental, please report any bugs or errors)
        Receive in-context examples of a specific text in your target language
        - `reverso <source_language_code> <target_language_code> <message>`
        examples:
            - `reverso en es the booking process was`
            - `-reverso de nl die frau`

        see `$langcodes` for a list of language codes

        The bot doesn't check for spelling so if you don't see any or few results,
        please make sure the input is spelled correctly
        """
        if lang_original not in helper_functions.language_codes or lang_original is None:
            return await ctx.send(NOT_FOUND_ERROR)

        elif lang_target not in helper_functions.language_codes or lang_target is None:
            return await ctx.send(NOT_FOUND_ERROR)

        elif message is None:
            return await ctx.send("Please enter the text you want translated\n eg. `$reverso es en lo que hicimos`")

        user_message = await ctx.send(embed=Embed(color=Color.nitro_pink(),
                                                  description="<a:loading:925770299188867105> Please wait"))

        self.languages = [lang_original, lang_target]
        self.user_input = message
        reverso_entries, results_found = self.get_entries(lang_original, lang_target, message)
        if results_found:
            reverso_pages = self.create_pages(reverso_entries)
            reverso_paginator = self.get_paginator(reverso_pages)
            await user_message.delete()
            await reverso_paginator.send(ctx, ephemeral=False)
        else:
            await user_message.delete()
            await ctx.send(f"No results. Please check your language codes and or spelling. "
                           f"Feel free to also checkout :\n{REVERSO_URL}")

    @staticmethod
    def get_entries(lang_1, lang_2, input_string):
        api = reverso(input_string, "", lang_1, lang_2)
        counter = 0
        examples = []
        for source, target in api.get_examples():
            exa = [helper_functions.highlight_example(source.text, source.highlighted),
                   helper_functions.highlight_example(target.text, target.highlighted)]
            examples.append(exa)
            counter += 1
            if counter == 10:
                break

        if len(examples) == 0:
            return [[]], False
        else:
            return examples, True

    def create_pages(self, entries):
        n_results = len(entries)
        if n_results == 0:
            print("No results found. Please make sure")
            return
        embeds = [self.result_embed(entry) for entry in entries]
        return embeds

    def result_embed(self, entry):
        embed = Embed(color=Color.nitro_pink())
        url = self.get_url()
        embed.description = f"<:reverso:925746938379386882> {helper_functions.language_codes[self.languages[0]]} -> " \
                            f"{helper_functions.language_codes[self.languages[1]]}\n"
        embed.title = f"{self.user_input.lower()}"
        embed.add_field(name=self.languages[0], value=entry[0], inline=False)
        embed.add_field(name=self.languages[1], value=entry[1], inline=False)
        embed.add_field(name="\u200b", value=f"[See original page on ReversoContext]({url})", inline=False)
        return embed

    @staticmethod
    def get_paginator(embedded_pages):
        paginator = pages.Paginator(pages=embedded_pages, show_disabled=False, show_indicator=True)
        paginator.customize_button("next", button_label=">", button_style=ButtonStyle.green)
        paginator.customize_button("prev", button_label="<", button_style=ButtonStyle.green)
        paginator.customize_button("first", button_label="<<", button_style=ButtonStyle.blurple)
        paginator.customize_button("last", button_label=">>", button_style=ButtonStyle.blurple)
        return paginator

    def get_url(self):
        url = f"{REVERSO_URL}{helper_functions.language_codes[self.languages[0]].lower()}-" \
              f"{helper_functions.language_codes[self.languages[1]].lower()}/{'+'.join(self.user_input.split())}"
        return url


def setup(bot):
    bot.add_cog(Reverso(bot))

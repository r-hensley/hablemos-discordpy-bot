# from .general import General as gen
# from .convo_starter import colors
#
# from random import choice
#
# from discord.ext import commands
# from discord import Embed
# from reverso_api.context import ReversoContextAPI
#
#
# # highlight keyword(s) in example
# def highlight_example(text, highlighted):
#     """'Highlights' ALL the highlighted parts of the word usage example with * characters.
#
#     Args:
#         text: The text of the example
#         highlighted: Indexes of the highlighted parts' indexes
#
#     Returns:
#         The highlighted word usage example
#
#     """
#
#     def insert_char(string, index, char):
#         """Inserts the given character into a string.
#
#         Example:
#             string = "abc"
#             index = 1
#             char = "+"
#             Returns: "a+bc"
#
#         Args:
#             string: Given string
#             index: Index where to insert
#             char: Which char to insert
#
#         Return:
#             String string with character char inserted at index index.
#         """
#
#         return string[:index] + char + string[index:]
#
#     def highlight_once(string, start, end, shift):
#         """'Highlights' ONE highlighted part of the word usage example with two * characters.
#
#         Example:
#             string = "This is a sample string"
#             start = 0
#             end = 4
#             shift = 0
#             Returns: "*This* is a sample string"
#
#         Args:
#             string: The string to be highlighted
#             start: The start index of the highlighted part
#             end: The end index of the highlighted part
#             shift: How many highlighting chars were already inserted (to get right indexes)
#
#         Returns:
#             The highlighted string.
#
#         """
#
#         s = insert_char(string, start + shift, "**")
#         s = insert_char(s, end + shift + 2, "**")
#         return s
#
#     shift = 0
#     for start, end in highlighted:
#         text = highlight_once(text, start, end, shift)
#         shift += 3
#     return text
#
#
# # determines if text is in Spanish or English or another language
# def english_or_spanish(string):
#     spa_conf = 0
#     eng_conf = 0
#     lang = detectlanguage.detect(string)
#     for i in range(len(lang)):
#         if lang[i]['language'] == 'es':
#             spa_conf = lang[i]['confidence']
#         if lang[i]['language'] == 'en':
#             eng_conf = lang[i]['confidence']
#     if spa_conf > eng_conf:
#         return ['es', 'en']
#     elif eng_conf > spa_conf:
#         return ['en', 'es']
#     elif spa_conf == 0 and eng_conf == 0:
#         return None
#     else:
#         return ['es', 'en']
#
#
# # Get the entries using the ReversoContext API
# def get_entries(text):
#     langs = english_or_spanish(text)
#     if langs is None:
#         return False
#     else:
#         api = ReversoContextAPI(text, "", langs[0], langs[1])
#         counter = 0
#         examples = list()
#         for source, target in api.get_examples():
#             exa = list()
#             exa.append(highlight_example(source.text, source.highlighted))
#             exa.append(highlight_example(target.text, target.highlighted))
#             examples.append(exa)
#             counter += 1
#             if counter == 4:
#                 break
#         if len(examples) == 0:
#             return False
#         return examples, langs
#
#
# def entries_embed(phrase, entries):
#     emb = Embed(colour=choice(colors))
#     emb.title = phrase
#
#     for ent in entries:
#         ent = f"{ent[0]}\n{ent[1]}"
#         emb.add_field(name=":small_orange_diamond:", value=ent, inline=False)
#
#     return emb
#
#
# def too_long_embed():
#     emb = Embed(colour=choice(colors))
#     emb.description = "❗The text you've entered is too long. Please try using a shorter one"
#     return emb
#
#
# def nothing_found_embed():
#     emb = Embed(colour=choice(colors))
#     emb.description = "I couldn't find any examples. There might be a typo or the language is not in English or Spanish"
#     return emb
#
#
# class Reverso(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
#
#     @commands.command(aliases=['ctx', 'contexto'])
#     @commands.cooldown(1, 7, type=commands.BucketType.user)
#     async def context(self, ctx, *text):
#         text = ' '.join(text)
#         if len(text) > 40:
#             await gen.safe_send(ctx.channel, ctx, embed=too_long_embed())
#             ctx.command.reset_cooldown(ctx)
#             return
#         entries = get_entries(text)
#         if entries:
#             await gen.safe_send(ctx.channel, ctx, embed=entries_embed(text, entries))
#         else:
#             await gen.safe_send(ctx.channel, ctx, embed=nothing_found_embed())
#             return
#
#
# def setup(bot):
#     bot.add_cog(Reverso(bot))

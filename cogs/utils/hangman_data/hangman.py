import asyncio
from random import choice
import time

from discord.ext import commands
from discord import Embed, File

from cogs.convo_starter import colors
from .hangman_help import get_unaccented_letter as gl, get_unaccented_word as gw, get_animal as ga, handle_spaces as hs, \
    get_random_image as gi

# strings for the embeds
DOES_NOT_EXIST = "{} La `{}` no se encuentra en esta palabra. Puedes volver a adivinar en 2 segundos"
ALREADY_GUESSED = "{} La `{}` ya se ha adivinado . Puedes volver a adivinar en 2 segundos"
CORRECT_GUESS = "{} ha adivinado la letra `{}`"
STARTED = "Nueva partida - **Animales**"
ON_GOING = "Ahorcado (Hangman) - **Animales**"
ENDED = "Ahorcado (Hangman) - Animales - Partida terminada"
WINNER = "¡Ganaste, **{}**! La palabra correcta era **{}** ({})"
LOSER = "Perdiste jeje. La palabra correcta era **{}** ({})"
TIME_OUT = "La sesión ha expirado"
SPA_ALPHABET = "aábcdeéfghiíjklmnñoópqrstuúüvwxyz"
ACCENTED_LETTERS = {'a': ['a', 'á'],
                    'e': ['e', 'é'],
                    'i': ['i', 'í'],
                    'o': ['o', 'ó'],
                    'u': ['u', 'ú', 'ü'], }
VOWELS = ['a', 'e', 'i', 'o', 'u']
MAX_ERRORS = 6
TIME_LIMIT = 2

back_slash = "\\"  # can't use back_slash in f-string


def embed_quote(header, state):
    embed = Embed(color=choice(colors))
    embed.title = header
    embed.description = state
    return embed


def final_embed(winner, animals, result=True):
    animal_image = gi(animals[1].replace(' ', ''))
    file = File(animal_image[0], filename=animal_image[1])
    embed = Embed(color=choice(colors))
    embed.title = ENDED
    embed.description = WINNER.format(winner, animals[0], animals[1]) if result else LOSER.format(animals[0], animals[1])
    embed.set_image(url=f"attachment://{animal_image[1]}")
    return file, embed


# new hangman
def start_game(word):
    return f"""
    `{' '.join(word)}`
    . ┌─────┐
    .┃...............┋
    .┃...............┋
    .┃
    .┃
    .┃ 
    /-\\
    """


class Hangman(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.errors = 0

    def get_hangman(self, message="", correctly_guest="", wrongly_guessed=""):
        return f"""
        {message}
        `{' '.join(correctly_guest)}`
        . ┌─────┐
        .┃...............┋
        .┃...............┋
        .┃{".............:cry:" if self.errors > 0 else ""}
        .┃{"............./" if self.errors > 1 else ""} {"|" if self.errors > 2 else ""} {back_slash if self.errors > 3 else ""}
        .┃{"............./" if self.errors > 4 else ""} {back_slash if self.errors > 5 else ""}
        /-\\    
        {' '.join(wrongly_guessed)}
        """

    def get_embed(self, letter, hidden_word, state_str, author, previously_guessed):
        if letter not in VOWELS:
            return embed_quote(ON_GOING, self.get_hangman(state_str.format(author, letter),
                                                          hidden_word,
                                                          previously_guessed))
        letra = '/'.join(ACCENTED_LETTERS[letter])
        return embed_quote(ON_GOING, self.get_hangman(state_str.format(author, letra),
                                                      hidden_word,
                                                      previously_guessed))

    # async def myf(self, ctx):
    #     embed = Embed()
    #     embed.title = "Cheese"
    #     embed.set_image(url=gi("Vulture"))
    #     embed.set_footer(text="cheese")
    #     await ctx.send(embed=embed)

    async def hangman(self, ctx):
        print("New game started")

        def check(m):
            return m.channel == ctx.channel
            # return m.author == ctx.author and m.channel == ctx.channel

        animales = ga()
        print(animales)
        word = animales[0].lower()
        word_list = list(word)
        word_without_accents = gw(word)
        na_word_list = list(word_without_accents)  # if user enters non-accented letter
        hidden_word = hs(list(word_without_accents))
        already_guessed = list()
        players = {}  # user: time

        emb_init = embed_quote(STARTED, start_game(hidden_word))
        await ctx.send(embed=emb_init)

        while True:
            user_guess = ""
            try:
                user_guess = await self.bot.wait_for('message', check=check, timeout=45)
            except asyncio.TimeoutError:
                await ctx.send(TIME_OUT)
                return

            user_id = user_guess.author.id
            user_name = user_guess.author
            # add player details to dict and check if user is not in cooldown
            if user_id not in players or time.time() - players[user_id] >= TIME_LIMIT:
                # Add player to players dictionary and check if cooled down
                players[user_id] = time.time()
                user_guess = user_guess.content.lower()
            else:
                continue

            if len(user_guess) == 1 and user_guess in SPA_ALPHABET:
                str_guess = gl(str(user_guess))  # get unaccented letter

                if str_guess in already_guessed:
                    emb = self.get_embed(str_guess, hidden_word, ALREADY_GUESSED, user_name, already_guessed)
                    await ctx.send(embed=emb)

                elif str_guess in na_word_list:
                    for i, c in enumerate(na_word_list):
                        if str_guess == c:
                            hidden_word[i] = word[i]

                    if hidden_word == word_list:
                        # Final guess is the last hidden letter
                        end_embed = final_embed(user_name, animales)
                        await ctx.send(file=end_embed[0], embed=end_embed[1])
                        return

                    # Guessed a letter correctly
                    players[user_id] = time.time() - TIME_LIMIT - 1  # no cooldown, guessed correctly
                    # I hate ternary operators
                    already_guessed.extend(
                        ACCENTED_LETTERS[str_guess]) if str_guess in VOWELS else already_guessed.append(str_guess)

                    emb = self.get_embed(str_guess, hidden_word, CORRECT_GUESS, user_name, already_guessed)
                    await ctx.send(embed=emb)

                else:
                    already_guessed.extend(
                        ACCENTED_LETTERS[str_guess]) if str_guess in VOWELS else already_guessed.append(str_guess)

                    self.errors += 1
                    emb = self.get_embed(str_guess, hidden_word, DOES_NOT_EXIST, user_name, already_guessed)

                    if self.errors > MAX_ERRORS:
                        end_embed = final_embed(user_name, animales, False)
                        await ctx.send(file=end_embed[0], embed=end_embed[1])
                        return

                    await ctx.send(embed=emb)

            elif user_guess in (word_without_accents, word):
                end_embed = final_embed(user_name, animales)
                await ctx.send(file=end_embed[0], embed=end_embed[1])
                return

            if user_guess == "quit":
                if ctx.author.id == user_id:
                    await ctx.send("Partida terminada")
                    return
                await ctx.send("Solo quién haya iniciado la partida la puede terminar.\n"
                               "De todos modos, la partida se va a terminar en 45 segundos si no se recibe ningún "
                               "input")

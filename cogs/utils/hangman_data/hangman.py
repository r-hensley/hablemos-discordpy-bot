import asyncio
from random import choice
import time
from re import sub

from discord.ext.commands import Cog
from discord import Embed, File

from cogs.convo_starter import colors
from cogs.utils.hangman_data.hangman_help import (get_unaccented_letter,
                                                  get_unaccented_word,
                                                  get_word as gw,
                                                  get_hidden_word,
                                                  get_random_image as gi)

# strings for the embeds
DOES_NOT_EXIST = "{} La `{}` no se encuentra en esta palabra. Puedes volver a adivinar en 2 segundos"
ALREADY_GUESSED = "{} La `{}` ya se ha adivinado . Puedes volver a adivinar en 2 segundos"
CORRECT_GUESS = "{} ha adivinado la letra `{}`"
STARTED = "Nueva partida - **{}**"
ON_GOING = "Ahorcado (Hangman) - **{}**"
ENDED = "Ahorcado (Hangman) - {} - Partida terminada"
WINNER = "¡Ganaste, **{}**! La palabra correcta era **{}** ({})"
LOSER = "Perdiste jeje. La palabra correcta era **{}** ({})"
TIME_OUT = "La sesión ha expirado"
SPA_ALPHABET = "aábcdeéfghiíjklmnñoópqrstuúüvwxyz"
VOWELS = {'a': ['a', 'á'],
          'e': ['e', 'é'],
          'i': ['i', 'í'],
          'o': ['o', 'ó'],
          'u': ['u', 'ú', 'ü'], }
MAX_ERRORS = 6
TIME_LIMIT = 2


def embed_quote(header, state):
    embed = Embed(color=choice(colors))
    embed.title = header
    embed.description = state
    return embed


def final_embed(winner, words, cat, result=True):
    animal_image = gi(words[1].replace(' ', ''), cat)
    file = File(animal_image[0], filename=animal_image[1])
    embed = Embed(color=choice(colors))
    embed.title = ENDED.format(cat)
    embed.description = WINNER.format(winner, words[0], words[1]) if result else LOSER.format(words[0],
                                                                                              words[1])
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


class Hangman(Cog):
    def __init__(self, bot, category):
        self.bot = bot
        self.errors = 0
        self.category = category

    def get_hangman(self, message="", correctly_guest="", wrongly_guessed=""):
        back_slash = "\\"  # can't use back_slash in f-string
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
        """
        Generates embed with hangman drawing, hidden word and guessed letters
        """
        if letter not in VOWELS:
            return embed_quote(ON_GOING.format(self.category), self.get_hangman(state_str.format(author, letter),
                                                                                hidden_word,
                                                                                previously_guessed))
        vowel = '/'.join(VOWELS[letter])
        return embed_quote(ON_GOING.format(self.category), self.get_hangman(state_str.format(author, vowel),
                                                                            hidden_word,
                                                                            previously_guessed))

    async def hangman(self, ctx):
        print("New game started")

        def check(m):
            return m.channel == ctx.channel
            # return m.author == ctx.author and m.channel == ctx.channel

        new_word = gw(self.category)  # [spanish, english]
        spa_word = sub('\/(.*)', '', new_word[0].lower())  # remove gendered part
        word_list = list(spa_word)
        word_without_accents = get_unaccented_word(spa_word)
        hidden_word = get_hidden_word(word_without_accents)
        already_guessed = list()
        players = {}  # user: time

        emb_init = embed_quote(STARTED.format(self.category), start_game(hidden_word))
        await ctx.send(embed=emb_init)

        while True:
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
                str_guess = get_unaccented_letter(user_guess)

                if str_guess in already_guessed:
                    emb = self.get_embed(str_guess, hidden_word, ALREADY_GUESSED, user_name, already_guessed)
                    await ctx.send(embed=emb)

                elif str_guess in word_without_accents:
                    for i, c in enumerate(word_without_accents):
                        if str_guess == c:
                            hidden_word[i] = spa_word[i]

                    if hidden_word == word_list:
                        # Final guess is the last hidden letter
                        end_embed = final_embed(user_name, new_word, self.category)
                        await ctx.send(file=end_embed[0], embed=end_embed[1])
                        return

                    # Guessed a letter correctly
                    players[user_id] = time.time() - TIME_LIMIT - 1  # no cooldown, guessed correctly
                    # I hate ternary operators
                    already_guessed.extend(
                        VOWELS[str_guess]) if str_guess in VOWELS else already_guessed.append(str_guess)

                    emb = self.get_embed(str_guess, hidden_word, CORRECT_GUESS, user_name, already_guessed)
                    await ctx.send(embed=emb)

                else:
                    already_guessed.extend(
                        VOWELS[str_guess]) if str_guess in VOWELS else already_guessed.append(str_guess)

                    self.errors += 1
                    emb = self.get_embed(str_guess, hidden_word, DOES_NOT_EXIST, user_name, already_guessed)

                    if self.errors > MAX_ERRORS:
                        end_embed = final_embed(user_name, new_word, self.category, False)
                        await ctx.send(file=end_embed[0], embed=end_embed[1])
                        return

                    await ctx.send(embed=emb)

            elif user_guess in (word_without_accents, spa_word):
                end_embed = final_embed(user_name, new_word, self.category)
                await ctx.send(file=end_embed[0], embed=end_embed[1])
                return

            if user_guess == "quit":
                if ctx.author.id == user_id:
                    await ctx.send("Partida terminada")
                    return
                await ctx.send("Solo quién haya iniciado la partida la puede terminar.\n"
                               "De todos modos, la partida se va a terminar en 45 segundos si no se recibe ningún "
                               "input")

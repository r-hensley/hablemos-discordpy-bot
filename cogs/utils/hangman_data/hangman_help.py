import os
from random import randint

dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

acentos = {
    'á': 'a',
    'é': 'e',
    'í': 'i',
    'ó': 'o',
    'ú': 'u',
    'ü': 'u',
}


def get_unaccented_word(word):
    no_accent = []
    for letter in list(word):
        if letter in list(acentos.keys()):
            no_accent.append(acentos[letter])
        else:
            no_accent.append(letter)

    return ''.join(no_accent)


def get_unaccented_letter(letter):
    if letter in list(acentos.keys()):
        return acentos[letter]
    return letter


def get_animal():
    with open(f"{dir_path}/hangman_data/ani_esp.txt", "r", encoding='utf 8') as f1, open(
            f"{dir_path}/hangman_data/ani_eng.txt", "r", encoding='utf 8') as f2:
        index = randint(0, 200)
        esp = f1.read().splitlines()[index]
        eng = f2.read().splitlines()[index]
    return esp, eng


# returns hidden string with space
def handle_spaces(word):
    word_arr = []
    for s in word:
        word_arr.append(' ') if s == ' ' else word_arr.append('◯')
    return word_arr

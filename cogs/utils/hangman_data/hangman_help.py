from os import path, walk
from random import randint, choice
from typing import List

dir_path = path.dirname(path.dirname(path.realpath(__file__)))

acentos = {
    'á': 'a',
    'é': 'e',
    'í': 'i',
    'ó': 'o',
    'ú': 'u',
    'ü': 'u',
}


def get_unaccented_word(word) -> List[str]:
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


def get_random_image(img: str):
    ani = []
    for root, _, files in walk(f"{dir_path}/hangman_data/animals_images/{img}"):

        for file in files:
            root_file_list = [f"{root}/{file}", f"{file}"]
            ani.append(root_file_list)

    return choice(ani)


# returns hidden string with space
def handle_spaces(word):
    word_arr = []
    for s in word:
        word_arr.append(' ') if s == ' ' else word_arr.append('◯')
    return word_arr

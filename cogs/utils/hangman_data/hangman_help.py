from os import path, walk
from random import choice
from csv import reader

dir_path = path.dirname(path.dirname(path.realpath(__file__)))

acentos = {
    'á': 'a',
    'é': 'e',
    'í': 'i',
    'ó': 'o',
    'ú': 'u',
    'ü': 'u',
}


def get_unaccented_word(word: str) -> str:
    no_accent = [acentos[letter] if letter in acentos else letter for letter in word]

    return ''.join(no_accent)


def get_unaccented_letter(letter):
    if letter in acentos:
        return acentos[letter]
    return letter


def get_word(category):
    with open(f"{dir_path}/hangman_data/{category}.csv", "r", encoding='utf 8') as animals_csv:
        result = reader(animals_csv)
        words = (choice(list(result)))
    return words[0], words[1]


def get_random_image(img, category):
    for root, _, files in walk(f"{dir_path}/hangman_data/{category}_images/{img}"):
        ani = [[f"{root}/{file}", f"{file}"] for file in files]
        return choice(ani)


# returns hidden string with space(s)
def get_hidden_word(word):
    return [' ' if s == ' ' else '◯' for s in word]  # faster than regex sub('[^\s]', '◯', string)

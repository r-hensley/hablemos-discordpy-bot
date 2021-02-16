import sqlite3

# Sqlite3 tables dictionary
tables = {'general': 'generales', 'personal': 'personales', 'tv': 'televisión', 'movies': 'películas',
          'books': 'libros', "music": 'música',
          'tech': 'tecnología', 'sport': 'deportes', 'food': 'comida_cocina', 'travel': 'viajes', 'fashion': 'ropa',
          'holi': 'feriados', 'edu': 'educación', 'strange': 'extrañas', 'phil': 'filo', 'lang': 'idiomas',
          'games': 'juegos', 'open': 'open'}

tables_keys = list(tables.keys())
tables_values = list(tables.values())

# SQLITE QUERY
connection = sqlite3.connect("cogs/utils/preguntas.db")
"""
SQLITE QUERY TO GET RANDOM QUESTION FROM SPECIFIED TABLE
{0} - English or Spanish question
{1} - topic/category
"""

SELECT_RANDOM_QUESTION = """
SELECT * FROM {0}
ORDER BY RANDOM()
LIMIT 1;
"""


def random_question(table):
    if table in tables_values:
        with connection:
            cursor = connection.cursor()
            cursor.execute(SELECT_RANDOM_QUESTION.format(table))
        return cursor.fetchone()
    return

# Below is a query and function to insert records into the database
#
# INSERT = 'INSERT INTO juegos (questions_spa, questions_eng) VALUES (?, ?);'
#
# def insert_into(lin1, lin2):
#     with connection:
#         connection.execute(INSERT, (lin1, lin2))
#
# with open("es.txt", "r", encoding='utf 8') as archivo1, open("en.txt", "r", encoding='utf 8') as archivo2:
#     for line1, line2 in zip(archivo1, archivo2):
#         lone_l = line1.strip()
#         ltwo_l = line2.strip()
#         insert_into(lone_l, ltwo_l)

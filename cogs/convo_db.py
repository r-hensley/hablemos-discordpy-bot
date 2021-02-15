import sqlite3
import re

tables = ['generales', 'personales', 'televisión', 'películas', 'libros', 'música',
          'móviles', 'aplicaciones', 'deportes', 'restaurantes', 'viajes', 'tecnología', 'ropa',
          'metas', 'temporadas', 'feriados', 'educación', 'comida_cocina', 'extrañas']

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
    if table in tables:
        with connection:
            cursor = connection.cursor()
            cursor.execute(SELECT_RANDOM_QUESTION.format(table))
        return cursor.fetchone()
    return "Invalid command Please see **!help topic**"

# Below is a query and function to insert records into the database

# INSERT = 'INSERT INTO filo (questions_spa, questions_eng) VALUES (?, ?);'

# def insert_into(lin1, lin2):
#     with connection:
#         connection.execute(INSERT, (lin1, lin2))

# with open("es.txt", "r", encoding='utf 8') as archivo1, open("en.txt", "r", encoding='utf 8') as archivo2:
#     for line1, line2 in zip(archivo1, archivo2):
#         lone_l = line1.strip()
#         ltwo_l = line2.strip()        
#         insert_into(lone_l, ltwo_l)

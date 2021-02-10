import sqlite3
import re

connection = sqlite3.connect("preguntas.db")

SELECT_RANDOM_QUESTION = """
SELECT questions FROM {0}
ORDER BY RANDOM()
LIMIT 1;
"""


def random_question(col):
    with connection:
        cursor = connection.cursor()
        cursor.execute(SELECT_RANDOM_QUESTION.format(col))
    return cursor.fetchone()[0]
    
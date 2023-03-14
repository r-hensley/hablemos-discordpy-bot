import sqlite3

'''
Schema:

- conversation_topics
    - id
    - english
    - spanish
'''

class Database:
    def __init__(self) -> None:
        pass
    
    def connect(self):
        self.conn = sqlite3.connect('hablemos.db')
        self.c = self.conn.cursor()

    def close(self):
        self.conn.close()
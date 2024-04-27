from aqt.qt import *
import sqlite3

from llm_word_parser.config import get_user_files_folder

db_path = os.path.join(get_user_files_folder(), 'llm_word_parser.db')


def setup_database():
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    # Create table if it doesn't exist
    cur.execute('''CREATE TABLE IF NOT EXISTS documents
                   (id INTEGER PRIMARY KEY, filename TEXT, content TEXT)''')
    cur.execute('''
                    CREATE TABLE IF NOT EXISTS dictionaries (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE,
                        path TEXT,
                        type INTEGER,
                        active INTEGER DEFAULT 1
                    )
    ''')
    con.commit()
    con.close()

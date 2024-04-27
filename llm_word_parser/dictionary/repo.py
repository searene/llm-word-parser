from aqt.utils import showInfo

from llm_word_parser.dictionary import Dictionary

import sqlite3


class DictionaryRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def add_scan_path(self, path: str):
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            try:
                cur.execute("INSERT INTO scan_paths (path) VALUES (?)", (path,))
                con.commit()
            except sqlite3.IntegrityError:
                showInfo("Path already exists.")

    def rescan_dictionaries(self):
        # Fetch all scan paths
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            cur.execute("SELECT path FROM scan_paths")
            paths = cur.fetchall()

        # Simulate scanning each path and adding dictionaries
        for path in paths:
            self.add_dictionary("Sample Dictionary", path[0])

    def add_dictionary(self, name: str, path: str):
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            try:
                cur.execute("INSERT INTO dictionaries (name, path) VALUES (?, ?)", (name, path))
                con.commit()
            except sqlite3.IntegrityError:
                showInfo("Dictionary already exists.")

    def remove(self, dictionary_id: int):
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            cur.execute("DELETE FROM dictionaries WHERE id = ?", (dictionary_id,))
            con.commit()

    def set_active_state(self, dictionary_id: int, active: bool):
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            cur.execute("UPDATE dictionaries SET active = ? WHERE id = ?", (1 if active else 0, dictionary_id))
            con.commit()

    def all_dictionaries(self):
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            cur.execute("SELECT id, name, path, active FROM dictionaries ORDER BY name")
            return [Dictionary(id=row[0], name=row[1], path=row[2], active=bool(row[3])) for row in cur.fetchall()]

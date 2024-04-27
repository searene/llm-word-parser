import glob
import os
import sqlite3
from typing import List

from llm_word_parser.dictionary import Dictionary, DictionaryType
from llm_word_parser.dictionary.mdict import MDict


class DictionaryRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def add_dictionary(self, name: str, path: str, dictionary_type: DictionaryType):
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            try:
                cur.execute("INSERT INTO dictionaries (name, path, type) VALUES (?, ?, ?)",
                            (name, path, dictionary_type.value))
                con.commit()
            except sqlite3.IntegrityError:
                print("Dictionary already exists.")

    def remove_dictionary(self, dictionary_id: int):
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            cur.execute("DELETE FROM dictionaries WHERE id = ?", (dictionary_id,))
            con.commit()

    def set_active_state(self, dictionary_id: int, active: bool):
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            cur.execute("UPDATE dictionaries SET active = ? WHERE id = ?", (1 if active else 0, dictionary_id))
            con.commit()

    def all_dictionaries(self) -> List[Dictionary]:
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            cur.execute("SELECT id, name, path, type, active FROM dictionaries ORDER BY name")
            dictionaries = []
            for row in cur.fetchall():
                id, name, path, type, active = row
                if type == 'mdict':
                    dictionaries.append(MDict(id=id, name=name, path=path, active=bool(active)))
                else:
                    raise ValueError(f"Unsupported dictionary type: {type}")
            return dictionaries

    def scan(self, directory: str):
        # Use os.path.join to create a path that includes all .mdx files in the given directory
        search_path = os.path.join(directory, "*.mdx")

        # Use glob.glob to get a list of all .mdx files in the directory
        mdict_files = glob.glob(search_path)

        # For each .mdx file found, add it to the repository
        for file_path in mdict_files:
            # Use the file name (without extension) as the dictionary name
            name = os.path.splitext(os.path.basename(file_path))[0]

            # Add the dictionary to the repository
            self.add_dictionary(name, file_path, DictionaryType.mdict)

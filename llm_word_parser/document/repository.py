import sqlite3

from llm_word_parser.config import set_default_document_id
from llm_word_parser.document import Document


class DocumentRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def add(self, document: Document) -> int:
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO documents (filename, content) VALUES (?, ?)", (document.filename, document.content))
            con.commit()
            return cur.lastrowid

    def remove(self, document_id: int):
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            cur.execute("DELETE FROM documents WHERE id = ?", (document_id,))
            con.commit()

    def set_as_default(self, document_id: int):
        set_default_document_id(document_id)

    def find_by_name(self, filename: str) -> Document:
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            cur.execute("SELECT id, filename, content FROM documents WHERE filename = ?", (filename,))
            row = cur.fetchone()
            if row is None:
                raise ValueError(f"Document with filename '{filename}' not found")
            return Document(id=row[0], filename=row[1], content=row[2])

    def all_documents(self) -> [Document]:
        print(self.db_path)
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            cur.execute("SELECT id, filename, content FROM documents")
            rows = cur.fetchall()
            return [Document(id=row[0], filename=row[1], content=row[2]) for row in rows]

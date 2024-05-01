import sqlite3
from typing import Optional, List

from llm_word_parser.config import set_default_document_id, get_default_document_id, remove_default_document
from llm_word_parser.db import get_db_path
from llm_word_parser.document import Document


class DocumentRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def add(self, document: Document) -> int:
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO documents (filename, content) VALUES (?, ?)", (document.filename, document.content))
            con.commit()
            res = cur.lastrowid
            if res is None:
                raise ValueError("Error while adding document")
            return res

    def remove(self, document_id: int) -> None:
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            cur.execute("DELETE FROM documents WHERE id = ?", (document_id,))
            con.commit()

    def find_by_id(self, doc_id: int) -> Document:
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            cur.execute("SELECT id, filename, content FROM documents WHERE id = ?", (doc_id,))
            row = cur.fetchone()
            if row is None:
                raise ValueError(f"Document with ID {doc_id} not found")
            return Document(id=row[0], filename=row[1], content=row[2])

    def get_default_document(self) -> Optional[Document]:
        doc_id = get_default_document_id()
        if doc_id is None:
            return None
        return self.find_by_id(doc_id)

    def set_as_default(self, document_id: int) -> None:
        set_default_document_id(document_id)

    def is_default(self, document_id: int) -> bool:
        return document_id == get_default_document_id()

    def remove_default(self) -> None:
        remove_default_document()

    def find_by_name(self, filename: str) -> Document:
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            cur.execute("SELECT id, filename, content FROM documents WHERE filename = ?", (filename,))
            row = cur.fetchone()
            if row is None:
                raise ValueError(f"Document with filename '{filename}' not found")
            return Document(id=row[0], filename=row[1], content=row[2])

    def all_documents(self) -> List[Document]:
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            cur.execute("SELECT id, filename, content FROM documents")
            rows = cur.fetchall()
            return [Document(id=row[0], filename=row[1], content=row[2]) for row in rows]

    def count(self) -> int:
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            cur.execute("SELECT COUNT(*) FROM documents")
            return cur.fetchone()[0]
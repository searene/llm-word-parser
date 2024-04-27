from typing import Optional


class Document:
    def __init__(self, id: Optional[int], filename: str, content: str):
        self.id = id
        self.filename = filename
        self.content = content

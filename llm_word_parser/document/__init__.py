from typing import Optional, List


class Document:
    def __init__(self, id: Optional[int], filename: str, content: str):
        self.id = id
        self.filename = filename
        self.content = content

    def get_contexts(self, word: str) -> List[str]:
        """Get all the paragraphs that contains the given word"""
        return [line for line in self.content.split("\n") if word in line]

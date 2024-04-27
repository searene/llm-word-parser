from typing import Optional

from llm_word_parser.dictionary import Dictionary, DictionaryType


class MDict(Dictionary):
    def __init__(self, id: Optional[int], name: str, path: str, active: bool = True):
        self.id = id
        self.name = name
        self.path = path
        self.type = DictionaryType.mdict
        self.active = active

    def query(self, word: str) -> str:
        pass
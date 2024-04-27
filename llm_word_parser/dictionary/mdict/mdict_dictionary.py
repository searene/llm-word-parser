from typing import Optional

from llm_word_parser.dictionary import Dictionary, DictionaryType
from llm_word_parser.dictionary.mdict.query.mdict_query import IndexBuilder


class MDict(Dictionary):
    def __init__(self, id: Optional[int], name: str, mdx_file_path: str, active: bool = True):
        self.id = id
        self.name = name
        self.path = mdx_file_path
        self.type = DictionaryType.mdict
        self.active = active
        self.mdx_builder = IndexBuilder(mdx_file_path)

    def query(self, word: str) -> Optional[str]:
        definitions = self.mdx_builder.mdx_lookup(word)
        return definitions[0] if definitions else None

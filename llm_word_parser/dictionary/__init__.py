from abc import ABC, abstractmethod
from llm_word_parser.dictionary.type import DictionaryType
from typing import Optional


class Dictionary(ABC):
    @abstractmethod
    def __init__(self, id: Optional[int], name: str, path: str, type: DictionaryType, active: bool = True):
        pass

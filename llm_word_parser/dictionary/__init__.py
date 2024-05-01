from abc import ABC, abstractmethod
from llm_word_parser.dictionary.type import DictionaryType
from typing import Optional


class Dictionary(ABC):
    @abstractmethod
    def __init__(self, id: Optional[int], name: str, path: str, type: DictionaryType, active: bool = True):
        pass

    @abstractmethod
    def query(self, word: str) -> Optional[str]:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def active(self) -> bool:
        pass

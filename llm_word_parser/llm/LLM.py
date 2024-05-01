from abc import ABC, abstractmethod


class LLM(ABC):

    @abstractmethod
    def answer(self, prompt: str) -> str:
        pass

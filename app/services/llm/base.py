from abc import ABC, abstractmethod

class LLM(ABC):
    @abstractmethod
    def extract(self, text: str) -> dict:
        raise NotImplementedError

# 🔧 alias: factory ve worker bunu bekliyor
LLMClient = LLM

from app.services.llm.base import LLM

class LocalOllamaLLM(LLM):
    def __init__(self, base_url: str):
        self.base_url = base_url

    def extract(self, text: str) -> dict:
        # placeholder
        return {"provider": "ollama", "data": {}}

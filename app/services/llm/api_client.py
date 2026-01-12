from app.services.llm.base import LLM

class ApiLLM(LLM):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def extract(self, text: str) -> dict:
        # placeholder
        return {"provider": "api", "data": {}}

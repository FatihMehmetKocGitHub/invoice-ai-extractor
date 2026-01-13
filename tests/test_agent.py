from app.services.agent.invoice_agent import run_agent
from app.services.llm.base import LLMClient

class DummyLLM(LLMClient):
    def complete_json(self, prompt: str):
        return {"fields": {}, "items": []}

def test_agent_runs_without_llm():
    out = run_agent("Ara Toplam: 1.000,00 TL", llm=None)
    assert "fields" in out and "items" in out and "warnings" in out

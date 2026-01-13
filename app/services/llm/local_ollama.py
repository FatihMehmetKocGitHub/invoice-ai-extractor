from __future__ import annotations

import json
import requests
from typing import Any, Dict

from app.services.llm.base import LLMClient


class OllamaLLM(LLMClient):
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def _chat(self, prompt: str) -> str:
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }
        r = requests.post(url, json=payload, timeout=60)
        r.raise_for_status()
        data = r.json()
        return data.get("response", "")

    def extract(self, text: str) -> Dict[str, Any]:
        prompt = (
            "Extract invoice data from the text below.\n"
            "Return ONLY valid JSON with keys: fields, items.\n\n"
            f"TEXT:\n{text}\n"
        )
        out = self._chat(prompt)
        return json.loads(out)

    def repair(self, text: str, current: Dict[str, Any]) -> Dict[str, Any]:
        prompt = (
            "You are given invoice text and current extracted JSON.\n"
            "Fix missing or wrong fields/items. Return ONLY JSON with keys you want to update.\n\n"
            f"TEXT:\n{text}\n\n"
            f"CURRENT_JSON:\n{json.dumps(current, ensure_ascii=False)}\n"
        )
        out = self._chat(prompt)
        return json.loads(out)

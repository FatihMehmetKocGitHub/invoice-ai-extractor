from __future__ import annotations
from typing import Optional

from app.core.config import settings
from app.services.llm.base import LLMClient
from app.services.llm.api_client import ApiLLMClient
from app.services.llm.local_ollama import OllamaLLMClient

def get_llm() -> Optional[LLMClient]:
    mode = (settings.LLM_MODE or "").lower().strip()
    if mode == "local":
        return OllamaLLMClient(model=settings.OLLAMA_MODEL)
    if mode == "api":
        return ApiLLMClient(
            base_url=settings.LLM_API_BASE_URL,
            api_key=settings.LLM_API_KEY,
            model=settings.LLM_API_MODEL,
        )
    return None

from __future__ import annotations
import os
from typing import Optional

from app.services.llm.base import LLMClient
from app.services.llm.local_ollama import OllamaLLM


def llm_enabled() -> bool:
    return os.getenv("USE_LLM", "0").lower() in ("1", "true", "yes", "on")


def get_llm() -> Optional[LLMClient]:
    if not llm_enabled():
        return None

    provider = os.getenv("LLM_PROVIDER", "ollama").lower()

    if provider == "ollama":
        base_url = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
        model = os.getenv("OLLAMA_MODEL", "llama3.1")
        return OllamaLLM(base_url=base_url, model=model)

    # future providers can be added here (openai, etc.)
    return None

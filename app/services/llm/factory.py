from __future__ import annotations

import os
from typing import Optional

from app.services.llm.base import LLM  # base.py'deki sınıf adı LLM


def llm_enabled() -> bool:
    return os.getenv("USE_LLM", "0").lower() in ("1", "true", "yes", "on")


def get_llm() -> Optional[LLM]:
    if not llm_enabled():
        return None

    provider = os.getenv("LLM_PROVIDER", "ollama").lower()

    if provider == "ollama":
        # lazy import: USE_LLM açık değilse requests vs hiç gerekmez
        from app.services.llm.local_ollama import OllamaLLM

        base_url = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
        model = os.getenv("OLLAMA_MODEL", "llama3.1")
        return OllamaLLM(base_url=base_url, model=model)

    return None

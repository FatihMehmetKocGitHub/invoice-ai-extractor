from __future__ import annotations
from pathlib import Path

_PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"

def load_prompt(name: str) -> str:
    p = _PROMPTS_DIR / name
    return p.read_text(encoding="utf-8")

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class LLMClient(ABC):
    """
    LLM interface. Must be optional: project runs without it.
    """

    @abstractmethod
    def extract(self, text: str) -> Dict[str, Any]:
        """Extract structured fields/items from raw/normalized invoice text."""
        raise NotImplementedError

    def repair(self, text: str, current: Dict[str, Any]) -> Dict[str, Any]:
        """
        Optional: Given current extraction output, return improvements.
        Default: no-op.
        """
        return {}

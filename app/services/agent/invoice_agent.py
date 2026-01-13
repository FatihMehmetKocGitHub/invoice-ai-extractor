from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from app.services.extraction.fields import extract_fields as rule_extract_fields
from app.services.extraction.items import extract_items as rule_extract_items
from app.services.postprocess.warnings import build_warnings
from app.services.llm.base import LLMClient
from app.services.llm.prompts import load_prompt


@dataclass
class AgentConfig:
    max_repairs: int = 1
    tol: float = 0.01


def _should_repair(warnings: List[str]) -> bool:
    # Minimum: subtotal/items mismatch, VAT mismatch, total mismatch
    return len(warnings) > 0


def run_agent(
    text: str,
    llm: Optional[LLMClient],
    config: AgentConfig = AgentConfig(),
) -> Dict[str, Any]:
    """
    Agent flow:
      1) Extract (rule-based baseline)
      2) Validate (warnings)
      3) Repair with LLM (optional) if warnings exist
      4) Re-validate
    """
    fields = rule_extract_fields(text)
    items = rule_extract_items(text)
    warnings = build_warnings(fields, items, tol=config.tol)

    debug: Dict[str, Any] = {
        "repairs_attempted": 0,
        "initial_warnings": warnings[:],
    }

    if llm and _should_repair(warnings) and config.max_repairs > 0:
        repaired = _repair_with_llm(text, fields, items, warnings, llm)
        debug["repairs_attempted"] += 1
        debug["repair_response"] = repaired.get("raw_response")

        # LLM'den dönene göre fields/items güncelle (güvenli parse)
        fields2, items2 = repaired.get("fields"), repaired.get("items")
        if isinstance(fields2, dict):
            fields = fields2
        if isinstance(items2, list):
            items = items2

        warnings = build_warnings(fields, items, tol=config.tol)

    debug["final_warnings"] = warnings[:]

    return {
        "fields": fields,
        "items": items,
        "warnings": warnings,
        "debug": debug,
    }


def _repair_with_llm(
    text: str,
    fields: Dict[str, Any],
    items: List[Dict[str, Any]],
    warnings: List[str],
    llm: LLMClient,
) -> Dict[str, Any]:
    prompt = load_prompt("repair_v1.txt").format(
        invoice_text=text,
        extracted_fields=fields,
        extracted_items=items,
        warnings=warnings,
    )
    resp = llm.complete_json(prompt)

    # resp: {"fields": {...}, "items": [...]} bekliyoruz.
    out: Dict[str, Any] = {"raw_response": resp}
    if isinstance(resp, dict):
        out["fields"] = resp.get("fields")
        out["items"] = resp.get("items")
    return out

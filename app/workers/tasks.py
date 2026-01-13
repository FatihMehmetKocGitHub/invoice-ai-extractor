from __future__ import annotations

import logging
from typing import Any, Dict

from app.workers.celery_app import celery_app
from app.storage.result_store import save_result
from app.services.extraction.pdf_text import extract_text_from_pdf
from app.services.extraction.ocr import ocr_pdf_if_needed
from app.services.postprocess.normalize import normalize_text
from app.services.agent.invoice_agent import run_agent, AgentConfig

logger = logging.getLogger(__name__)


@celery_app.task(name="process_invoice_task", bind=True)
def process_invoice_task(self, file_path: str) -> Dict[str, Any]:
    task_id = self.request.id
    logger.info("[TASK %s] processing %s", task_id, file_path)

    try:
        raw = extract_text_from_pdf(file_path)

        # OCR fallback if text is empty/too short
        if not raw or len(raw.strip()) < 30:
            raw = ocr_pdf_if_needed(file_path) or raw or ""

        clean = normalize_text(raw)

        llm = get_llm()
        agent_out = run_agent(
            clean,
            llm=llm,
            config=AgentConfig(max_repairs=1, tol=0.01),
        )

        result: Dict[str, Any] = {
            "raw_text": raw,
            "normalized_text": clean,
            "fields": agent_out.get("fields", {}),
            "items": agent_out.get("items", []),
            "warnings": agent_out.get("warnings", []),
            "debug": agent_out.get("debug", {}),
        }

        save_result(task_id, result)
        logger.info(
            "[TASK %s] done, chars=%s, items=%s, warnings=%s",
            task_id, len(clean), len(result["items"]), len(result["warnings"])
        )
        return result

    except Exception as e:
        # Save failure result so API can show it
        err = {"error": str(e), "file_path": file_path}
        save_result(task_id, {"status": "failed", **err})
        logger.exception("[TASK %s] failed: %s", task_id, e)
        raise

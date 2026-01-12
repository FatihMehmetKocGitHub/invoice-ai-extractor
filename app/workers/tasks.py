import uuid
from app.workers.celery_app import celery_app
from app.core.config import settings
from app.storage.result_store import ResultStore

store = ResultStore(settings.REDIS_URL)

@celery_app.task(name="process_invoice")
def process_invoice(filename: str) -> dict:
    # placeholder: burada ingestion/extraction/llm/validation/postprocess zinciri olacak
    result = {
        "filename": filename,
        "extracted": {"invoice_number": "DEMO-001", "total": 123.45},
        "status": "done",
    }
    return result

import uuid
from fastapi import APIRouter, UploadFile, File
from app.api.schemas.invoice import InvoiceResponse
from app.workers.tasks import process_invoice

router = APIRouter()

@router.post("/invoices", response_model=InvoiceResponse)
async def create_invoice(file: UploadFile = File(...)):
    # demo: sadece dosya adını işliyoruz (gerçekte temp storage vs)
    task = process_invoice.delay(file.filename)
    return InvoiceResponse(task_id=task.id, status="queued")

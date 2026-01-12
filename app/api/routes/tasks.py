from fastapi import APIRouter, HTTPException
from celery.result import AsyncResult
from app.workers.celery_app import celery_app
from app.api.schemas.invoice import InvoiceResponse

router = APIRouter()

@router.get("/tasks/{task_id}", response_model=InvoiceResponse)
def get_task(task_id: str):
    res = AsyncResult(task_id, app=celery_app)
    if res is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if res.successful():
        return InvoiceResponse(task_id=task_id, status="done", data=res.result)
    if res.failed():
        return InvoiceResponse(task_id=task_id, status="failed", errors=[str(res.result)])
    return InvoiceResponse(task_id=task_id, status=res.status.lower())

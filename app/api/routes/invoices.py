from fastapi import APIRouter, UploadFile, File
import os
import uuid

from app.workers.celery_app import celery_app

router = APIRouter()


@router.post("/invoices")
async def create_invoice(file: UploadFile = File(...)):
    # 1️⃣ temp klasörü garanti altına al
    os.makedirs("/tmp/invoices", exist_ok=True)

    # 2️⃣ benzersiz dosya adı
    file_id = str(uuid.uuid4())
    file_path = f"/tmp/invoices/{file_id}_{file.filename}"

    # 3️⃣ dosyayı diske yaz
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    # 4️⃣ Celery task'i NAME ile gönder (doğru yol)
    task = celery_app.send_task(
        "process_invoice_task",
        args=[file_path],
    )

    # 5️⃣ task id dön
    return {"task_id": task.id}

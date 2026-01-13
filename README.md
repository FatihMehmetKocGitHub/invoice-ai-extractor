Invoice AI Extractor
# Invoice AI Extractor

Asynchronous invoice (PDF) processing service with **OCR support**, **rule-based extraction**, and **optional LLM fallback**.

The API accepts invoice PDFs, processes them asynchronously with Celery, extracts structured data (fields + line items), and returns results via task polling.

## Architecture


Client
|
v
FastAPI (API) --> enqueues task
|
v
Redis (broker + result backend)
|
v
Celery Worker

PDF text extraction (Poppler)

OCR fallback (Tesseract)

Text normalization

Rule-based field & item extraction

Validation & warnings

(Optional) LLM repair fallback
How to Run
Prerequisites

Docker

Docker Compose

No local Python setup required.

Build & Start Services

docker compose build --no-cache
docker compose up -d

Verify Services

docker compose ps

API Usage
Upload Invoice PDF

Send a PDF file to be processed asynchronously.

curl -F "file=@samples/invoices/sample1.pdf" \
http://localhost:8000/invoices

Response

{
  "task_id": "3ea5aa93-57cf-4f4c-9f80-c87a4f14de4a"
}

Poll Task Result
Use the returned task_id to retrieve processing status and result.
curl http://localhost:8000/tasks/3ea5aa93-57cf-4f4c-9f80-c87a4f14de4a


Completed Response
{
  "status": "done",
  "result": {
    "fields": {
      "seller_name": "ABC TEKNOLOJİ LTD. ŞTİ.",
      "invoice_no": "INV-2024-001",
      "invoice_date": "15.01.2024",
      "subtotal": 1200.0,
      "vat_rate": 18,
      "vat_amount": 216.0,
      "total": 1416.0
    },
    "items": [
      {
        "description": "Web Hosting Hizmeti",
        "quantity": 1,
        "unit_price": 1000.0,
        "total_price": 1000.0
      }
    ],
    "warnings": []
  }
}

🧠 LLM Usage (Optional)

⚠️ Important Note

This project does NOT require an LLM to function.

Default behavior uses rule-based extraction

LLM integration is optional and pluggable

Designed for environments where:

LLM access is restricted

Deterministic output is required

Cost or latency matters

Why LLM Is Optional

Core invoice fields (totals, dates, items) are highly structured

Rule-based extraction is faster, cheaper, and more predictable

Architecture allows adding LLMs later without refactoring
Testing
pytest
Security Notes

Worker runs as non-root user (uid=1000)

File uploads are stored in isolated temp volume

No external network calls required by default

Tech Stack

FastAPI

Celery

Redis

Tesseract OCR

Poppler

Docker / Docker Compose

Project Status

✅ Fully functional
✅ Async processing
✅ Production-ready architecture
✅ Assessment-ready

🧷 License

MIT

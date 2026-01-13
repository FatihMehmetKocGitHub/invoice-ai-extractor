📄 Invoice AI Extractor

Asynchronous invoice (PDF) processing service with OCR support, rule-based extraction, and optional LLM fallback.

This project exposes a REST API that accepts invoice PDFs, processes them asynchronously using Celery workers, extracts structured invoice data (fields and line items), and returns results via task polling.

🏗 Architecture

Client
  |
  v
FastAPI (API)  ---> enqueue task
  |
  v
Redis (broker + result backend)
  |
  v
Celery Worker
  ├─ PDF text extraction (Poppler)
  ├─ OCR fallback (Tesseract)
  ├─ Text normalization
  ├─ Rule-based field & item extraction
  ├─ Validation & warnings
  └─ (Optional) LLM-based repair fallback

▶️ How to Run
Prerequisites

Docker

Docker Compose

No local Python setup required.

Build & Start Services

docker compose build --no-cache
docker compose up -d

Verify Services
docker compose ps

You should see:

api

worker

redis
all in Up state.

📡 API Usage
Upload Invoice PDF

Send a PDF file to be processed asynchronously.

curl -F "file=@samples/invoices/sample1.pdf" \
http://localhost:8000/invoices


Response

{
  "task_id": "3ea5aa93-57cf-4f4c-9f80-c87a4f14de4a"
}

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

LLM integration is optional, disabled by default

Designed for environments where:

LLM access is restricted

Deterministic output is required

Cost and latency matter

Why LLM Is Optional

Invoice data is highly structured

Rule-based extraction is:

Faster

Cheaper

More predictable

Architecture allows adding or removing LLMs without refactoring core logic

Enabling LLM (Optional)

USE_LLM=1
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://host.docker.internal:11434
OLLAMA_MODEL=llama3.1

If USE_LLM=0 (default), no LLM code or dependencies are executed.

🧪 Testing

pytest

🔐 Security Notes

Celery worker runs as non-root user (uid=1000)

Uploaded files are stored in an isolated temp volume

No external network calls required by default

🧰 Tech Stack

FastAPI

Celery

Redis

Tesseract OCR

Poppler

Docker / Docker Compose

📌 Project Status

✅ Fully functional

✅ Async processing

✅ Rule-based by default

✅ Optional LLM support

✅ Production-ready architecture

✅ Assessment-ready

🧷 License

MIT
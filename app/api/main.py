from fastapi import FastAPI
from app.api.routes.invoices import router as invoices_router
from app.api.routes.tasks import router as tasks_router

app = FastAPI(title="Invoice AI Extractor")

app.include_router(invoices_router)
app.include_router(tasks_router)

@app.get("/health")
def health():
    return {"status": "ok"}

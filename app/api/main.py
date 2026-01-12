from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import setup_logging
from app.api.routes.invoices import router as invoices_router
from app.api.routes.tasks import router as tasks_router

setup_logging()
app = FastAPI(title=settings.APP_NAME)

app.include_router(invoices_router, tags=["invoices"])
app.include_router(tasks_router, tags=["tasks"])

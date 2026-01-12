from pydantic import BaseModel
from typing import Any, Dict, Optional

class InvoiceResponse(BaseModel):
    task_id: str
    status: str
    data: Optional[Dict[str, Any]] = None
    errors: Optional[list[str]] = None

from pydantic import BaseModel
from typing import List, Optional


class InvoiceItem(BaseModel):
    description: str
    quantity: float
    unit_price: float
    total_price: float


class InvoiceResponse(BaseModel):
    invoice_number: str
    invoice_date: str
    supplier_name: str
    currency: str
    subtotal: float
    vat_rate: float
    vat_amount: float
    total_amount: float
    items: List[InvoiceItem]
    raw_text: Optional[str] = None

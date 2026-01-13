import re
from typing import Any, Dict, Optional


def _find(pattern: str, text: str, flags=re.IGNORECASE) -> Optional[str]:
    m = re.search(pattern, text, flags)
    if not m:
        return None
    return m.group(1).strip()


def _parse_tr_money(s: Optional[str]) -> Optional[float]:
    if not s:
        return None
    # "1.416,00" -> 1416.00
    s = s.replace(".", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def extract_fields(text: str) -> Dict[str, Any]:
    """
    Minimal alan çıkarımı: seller, tax_no, invoice_no, invoice_date, subtotal, vat_rate, vat_amount, total
    """
    result: Dict[str, Any] = {}

    # Seller adı: ilk satır
    lines = text.splitlines()
    first_line = lines[0].strip() if lines else None
    if first_line:
        result["seller_name"] = first_line

    result["tax_no"] = _find(r"Vergi No:\s*([0-9]{10,11})", text)
    result["invoice_no"] = _find(r"Fatura No:\s*([A-Z0-9\-\/]+)", text)
    result["invoice_date"] = _find(r"Fatura Tarihi:\s*([0-9]{2}\.[0-9]{2}\.[0-9]{4})", text)

    subtotal_raw = _find(r"Ara Toplam:\s*([0-9\.\,]+)", text)
    total_raw = _find(r"Genel Toplam:\s*([0-9\.\,]+)", text)

    result["subtotal"] = _parse_tr_money(subtotal_raw)
    result["total"] = _parse_tr_money(total_raw)

    m = re.search(r"KDV\s*\(%\s*([0-9]{1,2})\)\s*:\s*([0-9\.\,]+)", text, re.IGNORECASE)
    if m:
        result["vat_rate"] = int(m.group(1))
        result["vat_amount"] = _parse_tr_money(m.group(2))
    else:
        result["vat_rate"] = None
        result["vat_amount"] = None

    # Basit müşteri adı: "Müşteri" satırından sonraki satır
    for i, line in enumerate(lines):
        if line.strip().lower() == "müşteri" and i + 1 < len(lines):
            result["customer_name"] = lines[i + 1].strip()
            break

    return result

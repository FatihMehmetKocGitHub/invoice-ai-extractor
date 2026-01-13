from __future__ import annotations
from typing import Any, Dict, List, Optional


def _f(v: Optional[float]) -> str:
    if v is None:
        return "None"
    return f"{v:.2f}"


def build_warnings(
    fields: Dict[str, Any],
    items: List[Dict[str, Any]],
    tol: float = 0.01
) -> List[str]:
    warnings: List[str] = []

    # --- items subtotal ---
    items_subtotal = round(
        sum((i.get("total_price") or 0) for i in items),
        2
    ) if items else 0.0

    fields["items_subtotal"] = items_subtotal

    # --- compare invoice subtotal vs items subtotal ---
    invoice_subtotal = fields.get("subtotal")
    if invoice_subtotal is not None:
        if abs(invoice_subtotal - items_subtotal) > tol:
            warnings.append(
                f"Items subtotal ({_f(items_subtotal)}) "
                f"does not match invoice subtotal ({_f(invoice_subtotal)})"
            )

    # --- VAT check ---
    vat_rate = fields.get("vat_rate")
    vat_amount = fields.get("vat_amount")

    if invoice_subtotal is not None and vat_rate is not None and vat_amount is not None:
        # vat_rate may be 18 or 0.18 → normalize
        rate = vat_rate / 100.0 if vat_rate > 1 else vat_rate
        expected_vat = round(invoice_subtotal * rate, 2)

        if abs(expected_vat - vat_amount) > tol:
            warnings.append(
                f"VAT amount ({_f(vat_amount)}) "
                f"does not match expected ({_f(expected_vat)}) from subtotal*rate"
            )

    # --- total check ---
    total = fields.get("total") or fields.get("total_amount")
    if invoice_subtotal is not None and vat_amount is not None and total is not None:
        expected_total = round(invoice_subtotal + vat_amount, 2)

        if abs(expected_total - total) > tol:
            warnings.append(
                f"Total ({_f(total)}) "
                f"does not match expected ({_f(expected_total)}) from subtotal+VAT"
            )

    # --- item arithmetic check: qty * unit ≈ total ---
    for i in items or []:
        q = i.get("quantity")
        u = i.get("unit_price")
        t = i.get("total_price")

        if q is None or u is None or t is None:
            continue

        expected = round(float(q) * float(u), 2)

        if abs(expected - float(t)) > tol:
            warnings.append(
                f"Item '{i.get('description','')}' total ({_f(t)}) "
                f"does not match qty*unit ({_f(expected)})"
            )

    return warnings

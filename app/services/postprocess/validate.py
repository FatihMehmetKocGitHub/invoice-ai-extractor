from typing import Any, Dict, List, Tuple


def _sum_items(items: List[Dict[str, Any]]) -> float:
    total = 0.0
    for it in items or []:
        try:
            total += float(it.get("total_price") or 0.0)
        except (TypeError, ValueError):
            pass
    return round(total, 2)


def validate_and_enrich(fields: Dict[str, Any], items: List[Dict[str, Any]]) -> Tuple[Dict[str, Any], List[str]]:
    """
    - items toplamını hesaplar
    - fields.subtotal boşsa items toplamıyla doldurur
    - subtotal varsa, items toplamıyla farkı kontrol eder ve uyarı üretir
    """
    warnings: List[str] = []
    fields = fields or {}

    items_subtotal = _sum_items(items)
    fields["items_subtotal"] = items_subtotal

    subtotal = fields.get("subtotal")
    total = fields.get("total")

    # subtotal yoksa doldur
    if subtotal is None and items_subtotal > 0:
        fields["subtotal"] = items_subtotal
        warnings.append(f"subtotal boştu, items_subtotal ({items_subtotal}) ile dolduruldu.")

    # subtotal varsa karşılaştır
    try:
        if subtotal is not None:
            diff = round(float(subtotal) - items_subtotal, 2)
            if abs(diff) >= 0.01:  # kuruş toleransı
                warnings.append(f"subtotal ({subtotal}) ile items_subtotal ({items_subtotal}) uyuşmuyor. diff={diff}")
    except (TypeError, ValueError):
        warnings.append("subtotal sayısal değil, karşılaştırma yapılamadı.")

    # total vs subtotal+vat basit kontrol (vat varsa)
    try:
        vat_amount = fields.get("vat_amount")
        if total is not None and fields.get("subtotal") is not None and vat_amount is not None:
            calc_total = round(float(fields["subtotal"]) + float(vat_amount), 2)
            if abs(round(float(total) - calc_total, 2)) >= 0.01:
                warnings.append(f"total ({total}) ile subtotal+vat ({calc_total}) uyuşmuyor.")
    except (TypeError, ValueError):
        pass

    return fields, warnings

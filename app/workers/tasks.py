from app.services.llm.factory import get_llm
import os

# ...

def _needs_llm(fields: dict, items: list, warnings: list) -> bool:
    # kritik alanlar eksikse veya warning varsa
    critical = ["invoice_no", "invoice_date", "subtotal", "total"]
    missing = any(fields.get(k) in (None, "", 0) for k in critical)
    return missing or bool(warnings)

@celery_app.task(name="process_invoice_task")
def process_invoice_task(file_path: str):
    print(f"[TASK] processing {file_path}")

    raw = extract_text_from_pdf(file_path)
    clean = normalize_text(raw)

    fields = extract_fields(clean)
    items = extract_items(clean)
    warnings = build_warnings(fields, items)

    # OPTIONAL LLM fallback
    llm = get_llm()
    if llm is not None and _needs_llm(fields, items, warnings):
        try:
            current = {"fields": fields, "items": items}
            patch = llm.repair(clean, current) or {}

            # merge patch safely
            if isinstance(patch.get("fields"), dict):
                fields.update({k: v for k, v in patch["fields"].items() if v is not None})
            if isinstance(patch.get("items"), list) and patch["items"]:
                items = patch["items"]

            warnings = build_warnings(fields, items)
            warnings.append("LLM repair applied (optional).")
        except Exception as e:
            warnings.append(f"LLM repair failed (ignored): {type(e).__name__}: {e}")

    result = {
        "raw_text": raw,
        "normalized_text": clean,
        "fields": fields,
        "items": items,
        "warnings": warnings,
    }

    save_result(process_invoice_task.request.id, result)
    print(f"[TASK] done, chars={len(clean)}, items={len(items)}, warnings={len(warnings)}")
    return result

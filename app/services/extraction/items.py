import re
from typing import Any, Dict, List, Optional


_MONEY_RE = re.compile(r"(\d{1,3}(?:\.\d{3})*,\d{2})")  # 1.200,00 gibi


def _parse_tr_money(s: str) -> Optional[float]:
    """
    "1.416,00" -> 1416.00
    """
    s = s.strip()
    if not s:
        return None
    s = s.replace(".", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def _parse_qty(s: str) -> Optional[float]:
    s = s.strip()
    if not s:
        return None
    # 1 veya 1,5 gibi
    s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def extract_items(text: str) -> List[Dict[str, Any]]:
    """
    Satır kalemleri (items) için minimal parser.
    Beklenen satır formatı (örnek):
      Web Hosting Hizmeti 1 1.000,00 TL 1.000,00 TL
      Alan Adı (1 yıl)    1   200,00 TL   200,00 TL
    """
    items: List[Dict[str, Any]] = []
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

    # Header/özet satırlarını ayıklamak için basit filtre
    skip_prefixes = (
        "ürün", "hizmet", "adet", "birim", "fatura", "müşteri", "vergi", "adres",
        "ara toplam", "kdv", "genel toplam", "para birimi", "teşekkür",
    )

    for line in lines:
        low = " ".join(line.lower().split())  # fazla boşlukları normalize et

        # başlık/özet satırlarını atla
        if any(low.startswith(p) for p in skip_prefixes):
            continue

        # satırda en az 2 para değeri arıyoruz (birim fiyat + tutar)
        monies = list(_MONEY_RE.finditer(line))
        if len(monies) < 2:
            continue

        # son iki para değeri: unit_price, line_total
        unit_price_raw = monies[-2].group(1)
        line_total_raw = monies[-1].group(1)

        unit_price = _parse_tr_money(unit_price_raw)
        line_total = _parse_tr_money(line_total_raw)
        if unit_price is None or line_total is None:
            continue

        # unit_price'ın başladığı yere kadar olan kısım: "Açıklama + adet"
        prefix = line[:monies[-2].start()].strip()

        # prefix'in sonunda quantity var mı? (son token)
        parts = prefix.split()
        if len(parts) < 2:
            continue

        qty = _parse_qty(parts[-1])
        if qty is None:
            continue

        description = " ".join(parts[:-1]).strip()
        if not description:
            continue

        # currency: TR invoices -> TRY (TL görmesen de)
        currency = "TRY"

        items.append(
            {
                "description": description,
                "quantity": qty,
                "unit_price": unit_price,
                "total_price": line_total,
                "currency": currency,
                "raw_line": line,
            }
        )

    return items

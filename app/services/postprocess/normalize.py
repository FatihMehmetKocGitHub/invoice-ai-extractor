import re


def normalize_text(text: str) -> str:
    """
    PDF text extraction bazen kelime ortasına boşluk sokar: 'T oplam', 'F ATURA', 'L TD'
    Burada minimal ama etkili temizlik yapıyoruz.
    """
    if not text:
        return ""

    t = text

    # Satır sonlarını normalize et
    t = t.replace("\r\n", "\n").replace("\r", "\n")

    # Çoklu boşlukları tek boşluğa indir (satır içi)
    t = re.sub(r"[ \t]+", " ", t)

    # Bazı bariz parçalanmaları düzelt (heuristic)
    replacements = {
        "L TD.": "LTD.",
        "ŞTİ .": "ŞTİ.",
        "F ATURA": "FATURA",
        "F atura": "Fatura",
        "T oplam": "Toplam",
        "A ra": "Ara",
        "G enel": "Genel",
    }
    for k, v in replacements.items():
        t = t.replace(k, v)

    # "Kelime içi tek harf + boşluk + devam" durumlarını toparla (çok agresif değil)
    # Örn: "T arihi" -> "Tarihi", "F atura" zaten yukarıda
    t = re.sub(r"\b([A-Za-zÇĞİÖŞÜçğıöşü]) ([a-zçğıöşü]{2,})\b", r"\1\2", t)

    # Satır başı/sonu boşluklarını temizle
    t = "\n".join(line.strip() for line in t.split("\n"))

    # Boş satırları aşırı şişirmeyelim
    t = re.sub(r"\n{3,}", "\n\n", t)

    return t.strip()

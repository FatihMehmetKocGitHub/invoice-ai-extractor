from pathlib import Path
from typing import Optional
from pypdf import PdfReader


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract raw text from a text-based PDF.
    Returns a single concatenated string.
    """

    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    reader = PdfReader(str(path))
    pages_text = []

    for i, page in enumerate(reader.pages):
        try:
            text = page.extract_text()
            if text:
                pages_text.append(text)
        except Exception as e:
            # Sayfa bazlı hata yutulur ama loglanabilir
            pages_text.append(f"\n[ERROR reading page {i}]: {e}\n")

    full_text = "\n".join(pages_text).strip()

    return full_text

from __future__ import annotations
from typing import Optional
import subprocess
import tempfile
from pathlib import Path

def ocr_pdf_if_needed(file_path: str) -> Optional[str]:
    """
    Very simple OCR pipeline:
      - convert pdf pages to png via pdftoppm (poppler)
      - run tesseract on each image
    """
    pdf = Path(file_path)
    if not pdf.exists():
        return None

    with tempfile.TemporaryDirectory() as td:
        out_prefix = Path(td) / "page"
        # Convert PDF -> images
        # produces page-1.png, page-2.png...
        cmd = ["pdftoppm", "-png", str(pdf), str(out_prefix)]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception:
            return None

        texts = []
        for img in sorted(Path(td).glob("page-*.png")):
            base = img.with_suffix("")  # tesseract output base name
            try:
                subprocess.run(
                    ["tesseract", str(img), str(base), "-l", "eng"],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                txt_file = base.with_suffix(".txt")
                if txt_file.exists():
                    texts.append(txt_file.read_text(encoding="utf-8", errors="ignore"))
            except Exception:
                continue

        merged = "\n".join(t.strip() for t in texts if t.strip())
        return merged or None

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".webp"}


def _extract_with_pdfplumber(file_path: Path) -> Dict[str, Any]:
    import pdfplumber

    texts: List[str] = []
    tables: List[List[List[str]]] = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            texts.append(page.extract_text() or "")
            page_tables = page.extract_tables() or []
            tables.extend(page_tables)

    return {"text": "\n".join(t for t in texts if t).strip(), "tables": tables, "strategy": "pdfplumber"}


def _extract_with_tesseract(file_path: Path) -> Dict[str, Any]:
    import pytesseract
    from PIL import Image

    with Image.open(file_path) as image:
        text = pytesseract.image_to_string(image)
    return {"text": text.strip(), "tables": [], "strategy": "tesseract"}


def extract_text_and_tables(file_path: str, method: str = "auto") -> Dict[str, Any]:
    """
    Extract text (and when available, tables) from invoices/receipts.

    - `pdfplumber` for PDFs (text + tables)
    - `pytesseract` for image files (OCR text)
    """

    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    normalized_method = method.lower().strip()
    if normalized_method not in {"auto", "pdfplumber", "tesseract"}:
        raise ValueError("method must be one of: auto, pdfplumber, tesseract")

    if normalized_method == "pdfplumber":
        return _extract_with_pdfplumber(path)
    if normalized_method == "tesseract":
        return _extract_with_tesseract(path)

    if path.suffix.lower() == ".pdf":
        return _extract_with_pdfplumber(path)
    if path.suffix.lower() in IMAGE_EXTENSIONS:
        return _extract_with_tesseract(path)

    raise ValueError(
        "auto method only supports PDF files for pdfplumber and common image files for tesseract OCR"
    )

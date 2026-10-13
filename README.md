# WebDev-Ayush-Document-Information-Extraction-Pipeline-Invoice-Parser-LLM-OCR-

Minimal starter structure for invoice/receipt information extraction:

- `invoice_parser/extract.py`
  - `pdfplumber` based extraction for PDF text/tables.
  - `pytesseract` based OCR extraction for image files.
- `invoice_parser/llm_prompt.py`
  - OpenAI/LangChain/Instructor-ready prompt helpers.
  - Pydantic schema output via `InvoiceData`.
- `invoice_parser/models.py`
  - Pydantic models for invoice JSON schema.
- `test_invariants.py`
  - Small validation script that checks invoice totals invariants.

## GitHub search queries

- `invoice-parser pydantic langchain`
- `document-information-extraction llm json`
- `receipt-parser-tesseract-openai`
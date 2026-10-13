from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List

from invoice_parser.models import InvoiceData


def _is_close(a: float, b: float, tolerance: float = 0.01) -> bool:
    return abs(a - b) <= tolerance


def validate_invoice_invariants(invoice: InvoiceData, tolerance: float = 0.01) -> List[str]:
    errors: List[str] = []

    computed_subtotal = 0.0
    for idx, item in enumerate(invoice.line_items, start=1):
        expected_line_total = item.quantity * item.unit_price
        if not _is_close(item.line_total, expected_line_total, tolerance):
            errors.append(
                f"line_items[{idx}] line_total mismatch: expected {expected_line_total:.2f}, got {item.line_total:.2f}"
            )
        computed_subtotal += item.line_total

    if not _is_close(invoice.subtotal, computed_subtotal, tolerance):
        errors.append(
            f"subtotal mismatch: expected {computed_subtotal:.2f}, got {invoice.subtotal:.2f}"
        )

    expected_total = invoice.subtotal + invoice.tax - invoice.discount
    if not _is_close(invoice.total, expected_total, tolerance):
        errors.append(f"total mismatch: expected {expected_total:.2f}, got {invoice.total:.2f}")

    return errors


def _run_self_test() -> int:
    sample = InvoiceData.model_validate(
        {
            "invoice_number": "INV-1001",
            "line_items": [
                {"description": "Item A", "quantity": 2, "unit_price": 50, "line_total": 100},
                {"description": "Item B", "quantity": 1, "unit_price": 25, "line_total": 25},
            ],
            "subtotal": 125,
            "tax": 12.5,
            "discount": 2.5,
            "total": 135,
        }
    )
    errors = validate_invoice_invariants(sample)
    if errors:
        for error in errors:
            print(f"[FAIL] {error}")
        return 1
    print("[PASS] self-test invariants are valid")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate invoice total invariants.")
    parser.add_argument("--file", type=Path, help="Path to invoice JSON file")
    parser.add_argument("--self-test", action="store_true", help="Run built-in sample validation")
    args = parser.parse_args()

    if args.self_test:
        return _run_self_test()

    if not args.file:
        raise SystemExit("Provide --file <invoice.json> or use --self-test")

    data = json.loads(args.file.read_text(encoding="utf-8"))
    invoice = InvoiceData.model_validate(data)
    errors = validate_invoice_invariants(invoice)

    if errors:
        for error in errors:
            print(f"[FAIL] {error}")
        return 1

    print("[PASS] invoice invariants validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

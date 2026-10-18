"""
Keeps invoice numbers unique across runs.

The last number used is saved in invoice_counter.json, so the next run
continues from there instead of starting again at 001 — two invoices with
the same number would be a real problem for a client's bookkeeping, and
the old PDFs would be overwritten.
"""

import json
from pathlib import Path

COUNTER_PATH = Path("invoice_counter.json")


def last_invoice_number(path=COUNTER_PATH):
    try:
        with open(path) as f:
            return int(json.load(f)["last_invoice_number"])
    except (FileNotFoundError, KeyError, ValueError, json.JSONDecodeError):
        return 0


def save_invoice_number(number, path=COUNTER_PATH):
    with open(path, "w") as f:
        json.dump({"last_invoice_number": number}, f)

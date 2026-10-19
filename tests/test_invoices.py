from datetime import date
from decimal import Decimal

import pytest

from generators.pdf_builder import build_invoice
from processors.calculator import build_invoice_data, calculate_tax, to_cents
from processors.numbering import last_invoice_number, save_invoice_number
from processors.reader import ClientInvoice, get_clients


# --- money ---------------------------------------------------------------

@pytest.mark.parametrize(
    "value, rounded",
    [("10.005", "10.01"), ("10.004", "10.00"), ("2.675", "2.68"), ("7", "7.00")],
)
def test_rounds_half_cents_up(value, rounded):
    assert to_cents(Decimal(value)) == Decimal(rounded)


def test_tax_is_exact_to_the_cent():
    # 0.1 + 0.2 style float errors would show up here
    assert calculate_tax(Decimal("19.99"), Decimal("13")) == Decimal("2.60")


def test_invoice_totals():
    client = ClientInvoice(
        client_name="John Smith", service="Web Scraping", amount="150", tax_rate="13", due_date="2026-06-15"
    )
    data = build_invoice_data(client)
    assert data["amount"] == Decimal("150.00")
    assert data["tax_amount"] == Decimal("19.50")
    assert data["total"] == Decimal("169.50")
    assert data["due_date"] == "2026-06-15"


# --- reading the CSV -----------------------------------------------------

def write_csv(tmp_path, rows):
    path = tmp_path / "clients.csv"
    path.write_text("client_name, service, amount, tax_rate, due_date\n" + "\n".join(rows) + "\n")
    return path


def test_good_rows_are_read(tmp_path):
    path = write_csv(tmp_path, ["John Smith, Web Scraping, 150, 13, 2026-06-15"])
    clients, errors = get_clients(path)
    assert errors == []
    assert clients[0].client_name == "John Smith"
    assert clients[0].amount == Decimal("150")
    assert clients[0].due_date == date(2026, 6, 15)


def test_bad_rows_are_skipped_with_their_row_number(tmp_path):
    path = write_csv(
        tmp_path,
        [
            "John Smith, Web Scraping, 150, 13, 2026-06-15",
            "Sara Lee, Data Analysis, -5, 13, 2026-06-20",   # negative amount
            ", Consulting, 100, 13, 2026-06-20",               # no name
            "Ana Diop, Design, 100, 150, 2026-06-20",          # tax over 100%
            "Bo Chen, API work, 100, 13, 20-06-2026",          # wrong date format
        ],
    )
    clients, errors = get_clients(path)
    assert [c.client_name for c in clients] == ["John Smith"]
    assert [e.split(":")[0] for e in errors] == ["Row 3", "Row 4", "Row 5", "Row 6"]
    assert "amount" in errors[0]
    assert "client_name" in errors[1]
    assert "tax_rate" in errors[2]
    assert "due_date" in errors[3]


def test_sample_input_file_is_valid():
    clients, errors = get_clients("input/clients.csv")
    assert clients and errors == []


# --- invoice numbers -------------------------------------------------------

def test_numbering_starts_at_zero_and_continues(tmp_path):
    counter = tmp_path / "invoice_counter.json"
    assert last_invoice_number(counter) == 0
    save_invoice_number(7, counter)
    assert last_invoice_number(counter) == 7


def test_broken_counter_file_starts_again_instead_of_crashing(tmp_path):
    counter = tmp_path / "invoice_counter.json"
    counter.write_text("not json")
    assert last_invoice_number(counter) == 0


# --- the PDF -------------------------------------------------------------

def test_builds_a_pdf_with_a_safe_file_name(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)  # the builder writes into ./output
    client = ClientInvoice(
        client_name="A/B Traders", service="Scraping", amount="99.99", tax_rate="13", due_date="2026-06-15"
    )
    path = build_invoice(build_invoice_data(client), invoice_number="042")
    assert path.name == "Invoice_ABTraders_042.pdf"
    assert path.read_bytes().startswith(b"%PDF")

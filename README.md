# csv-to-invoice

[![CI](https://github.com/maniesh-lab/csv-to-invoice/actions/workflows/ci.yml/badge.svg)](https://github.com/maniesh-lab/csv-to-invoice/actions/workflows/ci.yml)

Turns a CSV of clients into one PDF invoice each. Every row is checked with
Pydantic, money is worked out with `Decimal` so cents are never off, and invoice
numbers carry on between runs so old invoices are never overwritten. A bad row is
skipped with a message instead of stopping the batch.

---

## Features

- Generate one PDF invoice per CSV row
- Automatic tax and total calculations, done with `Decimal` and rounded to the cent (no floating-point money errors)
- CSV validation with Pydantic — names can't be blank, amounts must be positive, tax rates 0–100, due dates must be real dates
- Bad rows are skipped with a clear message (e.g. `Row 3: due_date: ...`) instead of stopping the whole batch
- Clean, professional invoice layout
- Sequential invoice numbering that continues across runs (saved in `invoice_counter.json`), so numbers are never reused and old PDFs are never overwritten
- Easy template customization

---

## Project Structure

```
csv-to-invoice/
│
├── templates/
│   ├── __init__.py
│   └── invoice_template.py    # colors, fonts, layout, sender info
│
├── processors/
│   ├── __init__.py
│   ├── reader.py              # loads and validates CSV with Pydantic
│   ├── calculator.py          # tax, subtotal, and total logic (Decimal)
│   └── numbering.py           # remembers the last invoice number between runs
│
├── generators/
│   ├── __init__.py
│   └── pdf_builder.py         # builds and exports PDF using fpdf2
│
├── input/
│   └── clients.csv            # sample input
│
├── output/                    # generated invoices land here (6 samples included)
├── screenshots/
│   └── invoice_preview.png
│
├── tests/
│   └── test_invoices.py       # money, validation, numbering and the PDF
│
├── .github/workflows/ci.yml   # lint + tests on every push (Python 3.11–3.13)
├── main.py                    # orchestrates the full pipeline
├── .gitignore
├── pytest.ini
├── ruff.toml                  # lint rules
├── requirements.txt
├── requirements-test.txt      # + pytest and ruff for tests and lint
├── LICENSE
└── README.md
```

---

## How to Run

**1. Clone the repo**
```bash
git clone https://github.com/maniesh-lab/csv-to-invoice
cd csv-to-invoice
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add your client data to `input/clients.csv`**
```csv
client_name, service, amount, tax_rate, due_date
John Smith, Web Scraping, 150, 13, 2026-06-15
```

**5. Run the pipeline**
```bash
python main.py
```

Generated invoices appear in the `output/` folder. Any row that fails
validation is listed in the terminal and skipped; the rest are still created.

Invoice numbers pick up where the last run stopped. To start again from
`001`, delete `invoice_counter.json`.

**Run the tests**
```bash
pip install -r requirements.txt -r requirements-test.txt
pytest
ruff check .
```
They check the money maths (rounding to the cent), that bad rows are skipped
with the right row number, that invoice numbers carry on between runs, and that
a real PDF is written.
GitHub Actions runs them, plus a `ruff` lint check, on Python 3.11–3.13 for
every push (pandas 3 needs Python 3.11 or newer).

---

## Sample Invoice

![Invoice Preview](screenshots/invoice_preview.png)

---

## Customization

All invoice styling lives in `templates/invoice_template.py` — update your name,
email, colors, and fonts there without touching any other file.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| `pandas` | CSV reading |
| `pydantic` | Data validation |
| `fpdf2` | PDF generation |
| `pathlib` | File path handling |
| `pytest` | Tests |
| `ruff` | Lint check, run with the tests by GitHub Actions on every push |

---

## Use Case

Built for small business owners who manage client billing in spreadsheets and
need a fast, automated way to produce professional invoices — no manual formatting,
no per-client effort.

---

## Known Limitations

- Each invoice has one line: one service and one amount per CSV row
- Amounts are always shown in US dollars (`$`)
- Run `main.py` from the repo folder: `input/`, `output/` and `invoice_counter.json` are found from where you run it

---

## Author

**Manish Pandeya** · [github.com/maniesh-lab](https://github.com/maniesh-lab)

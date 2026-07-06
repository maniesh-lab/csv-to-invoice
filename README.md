# csv-to-invoice

Automatically generate professional PDF invoices from a CSV spreadsheet.
Drop in a CSV containing client names, services, and amounts — get a polished,
ready-to-send PDF invoice per client in seconds.

---

## Features

- Generate one PDF invoice per CSV row
- Automatic tax and total calculations
- CSV validation with Pydantic
- Clean, professional invoice layout
- Sequential invoice numbering
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
│   └── calculator.py          # tax, subtotal, and total logic
│
├── generators/
│   ├── __init__.py
│   └── pdf_builder.py         # builds and exports PDF using fpdf2
│
├── input/
│   └── clients.csv            # sample input
│
├── output/                    # generated invoices land here
├── main.py                    # orchestrates the full pipeline
├── .gitignore
├── requirements.txt
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

Generated invoices appear in the `output/` folder.


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

---

## Use Case

Built for small business owners who manage client billing in spreadsheets and
need a fast, automated way to produce professional invoices — no manual formatting,
no per-client effort.

---

## Author

**Manish Pandeya** · [github.com/maniesh-lab](https://github.com/maniesh-lab)
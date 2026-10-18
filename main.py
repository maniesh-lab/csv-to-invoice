from generators.pdf_builder import build_invoice
from processors.calculator import build_invoice_data
from processors.numbering import last_invoice_number, save_invoice_number
from processors.reader import get_clients

CSV_PATH = "input/clients.csv"


def main():
    clients, errors = get_clients(CSV_PATH)

    for error in errors:
        print(f"Skipped — {error}")

    number = last_invoice_number()
    for client in clients:
        number += 1
        invoice_data = build_invoice_data(client)
        filename = build_invoice(invoice_data, invoice_number=f"{number:03d}")
        save_invoice_number(number)  # saved after each one, so a crash never reuses a number
        print(f"Generated: {filename}")

    print(f"\nDone: {len(clients)} invoice(s) created, {len(errors)} row(s) skipped.")


if __name__ == "__main__":
    main()

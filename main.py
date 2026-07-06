from processors.reader import get_clients
from processors.calculator import build_invoice_data
from generators.pdf_builder import build_invoice

CSV_PATH = "input/clients.csv"

def main():
    clients = get_clients(CSV_PATH)
    for i, client in enumerate(clients, start=1):
        invoice_data = build_invoice_data(client)
        filename = build_invoice(invoice_data, invoice_number=f"{i:03d}")
        print(f"Generated: {filename}")

if __name__ == "__main__":
    main()
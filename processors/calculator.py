from decimal import ROUND_HALF_UP, Decimal

CENT = Decimal("0.01")


def to_cents(value):
    """Round money to 2 decimal places the way invoices do (0.005 -> 0.01)."""
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def calculate_tax(amount, tax_rate):
    return to_cents(amount * tax_rate / 100)


def calculate_total(amount, tax_amount):
    return to_cents(amount + tax_amount)


def build_invoice_data(client):
    tax_amount = calculate_tax(client.amount, client.tax_rate)
    total = calculate_total(client.amount, tax_amount)

    return {
        "client_name": client.client_name,
        "service": client.service,
        "amount": to_cents(client.amount),
        "tax_rate": client.tax_rate,
        "tax_amount": tax_amount,
        "total": total,
        "due_date": client.due_date.isoformat(),
    }

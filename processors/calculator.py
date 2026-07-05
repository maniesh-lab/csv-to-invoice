def calculate_tax(amount, tax_rate):
    return amount * (tax_rate / 100)


def calculate_total(amount, tax_amount):
    return amount + tax_amount
    

def build_invoice_data(client):
    tax_amount = calculate_tax(client.amount, client.tax_rate)
    total = calculate_total(client.amount, tax_amount)

    return{
        "client_name":client.client_name,
        "service": client.service,
        "amount": client.amount,
        "tax_rate": client.tax_rate,
        "tax_amount": tax_amount,
        "total": total,
        "due_date": client.due_date
    }
import pandas as pd
from pydantic import BaseModel


class ClientInvoice(BaseModel):
    client_name: str
    service: str
    amount: float
    tax_rate: float
    due_date: str



def load_csv(filepath):
    row_data = pd.read_csv(filepath)
    row_data = pd.read_csv(filepath, skipinitialspace=True)  # removes blank spaces right after a comma in data file
    return row_data



def validate_row(row):
    return ClientInvoice(
        client_name=row["client_name"],
        service=row["service"],
        amount=row["amount"],
        tax_rate=row["tax_rate"],
        due_date=row["due_date"]
    )



def get_clients(filepath):
    df = load_csv(filepath)         
    clients = []
    for _, row in df.iterrows():      
        client = validate_row(row)   
        clients.append(client)    
    return clients

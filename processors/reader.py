from datetime import date
from decimal import Decimal

import pandas as pd
from pydantic import BaseModel, Field, ValidationError


class ClientInvoice(BaseModel):
    client_name: str = Field(min_length=1)
    service: str = Field(min_length=1)
    # Decimal, not float: floats can't store most cents exactly
    # (0.1 + 0.2 == 0.30000000000000004), which is wrong for money.
    amount: Decimal = Field(gt=0)
    tax_rate: Decimal = Field(ge=0, le=100)
    due_date: date  # must be a real date like 2026-06-15


def load_csv(filepath):
    # skipinitialspace removes the blank space right after each comma.
    # dtype=str keeps every value as text so pandas doesn't turn amounts into
    # floats first; Pydantic converts and checks each field itself.
    return pd.read_csv(filepath, skipinitialspace=True, dtype=str, keep_default_na=False)


def get_clients(filepath):
    """Read and validate every row.

    Returns (clients, errors): the rows that passed, and a readable message
    for each row that didn't, so one bad row doesn't stop the whole batch.
    """
    df = load_csv(filepath)
    clients = []
    errors = []

    # start=2: row 1 of the file is the header, so the first data row is row 2
    for row_number, row in enumerate(df.to_dict(orient="records"), start=2):
        try:
            clients.append(ClientInvoice(**row))
        except ValidationError as e:
            problems = "; ".join(f"{err['loc'][0]}: {err['msg']}" for err in e.errors())
            errors.append(f"Row {row_number}: {problems}")

    return clients, errors

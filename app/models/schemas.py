from datetime import date
from pydantic import BaseModel
from typing import List

class Transaction(BaseModel):
    date: date
    transaction: str
    amount: float
    description: str
    category: str
    is_direct: bool

class BankStatementResponse(BaseModel):
    transactions: List[Transaction]
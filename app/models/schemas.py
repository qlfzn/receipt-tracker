from pydantic import BaseModel
from typing import Optional, List

class ReceiptUploadResponse(BaseModel):
    filename: str
    extracted_text: str
    message: str

class ReceiptItem(BaseModel):
    name: str
    quantity: Optional[int]
    unit_price: Optional[float]
    total_price: Optional[float]
    category: Optional[str]
    type: Optional[str]

class ParsedReceipt(BaseModel):
    merchant_name: str
    transaction_date: Optional[str]
    items: List[ReceiptItem] = []
    type: str
    subtotal: Optional[float] = None
    total_amount: Optional[float]

class HealthCheckResponse(BaseModel):
    status: str
    message: str
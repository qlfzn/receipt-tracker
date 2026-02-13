from pydantic import BaseModel

class ReceiptUploadResponse(BaseModel):
    filename: str
    extracted_text: str
    message: str

class HealthCheckResponse(BaseModel):
    status: str
    message: str
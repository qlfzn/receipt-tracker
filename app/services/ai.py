import os
import json
from typing import Type, Dict
from dotenv import load_dotenv
from groq import Groq
from app.models.schemas import ParsedReceipt
from pydantic import BaseModel, ValidationError

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(
    api_key=API_KEY,
    max_retries=3,
)

class AIExtractionError(Exception):
    pass

class SchemaValidationError(Exception):
    pass

def generate_formatted_data(parsed_text: str) -> Dict:
    """
    Extract structured receipt data from raw text.
    """
    schema = ParsedReceipt.model_json_schema()
    
    example = """
    Example input:
    (Receipt)
    "Supermarket
    Date: 01/15/2026
    
    Milk 2.0 $3.99 $7.98
    Bread 1.0 $2.49 $2.49
    
    Subtotal: $10.47
    Tax: $1.10
    Discount: $0.50
    Total: $11.31"
    
    Example output:
    {
        "merchant_name": "Supermarket",
        "transaction_date": "2026-01-15",
        "items": [
            {"name": "Milk", "quantity": 2.0, "unit_price": 3.99, "total_price": 7.98, "category": null},
            {"name": "Bread", "quantity": 1.0, "unit_price": 2.49, "total_price": 2.49, "category": null}
        ],
        "type": "receipt"
        "subtotal": 10.47,
        "tax": 1.10,
        "discount": 0.50,
        "total_amount": 11.31,
        "confidence_score": 0.95
    }
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"""
                    You are a receipt data extraction expert. Extract structured information from receipt text and return ONLY valid JSON.
                    Schema to follow: {json.dumps(schema, indent=2)}
                    
                    Rules:
                    - Return ONLY valid JSON, no markdown or explanation
                    - If it is not receipt, it might be proof of payment file. Please structure the extracted text from proof of payment based on the same schema.
                    - Use null for missing optional fields
                    - Format dates as YYYY-MM-DD when possible
                    - Use decimal numbers for prices
                    - Estimate confidence_score (0.0-1.0) based on text clarity
                    - If you cannot extract required fields (subtotal, items, total_amount), set confidence_score < 0.5
                    """
                },
                {
                    "role": "user",
                    "content": f"{example}\n\nNow extract from this receipt:\n\n{parsed_text}"
                }
            ],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"},
            temperature=0.1,
        )
        
        response_text = chat_completion.choices[0].message.content
        
        try:
            parsed_json = json.loads(str(response_text))
            return parsed_json
        except json.JSONDecodeError as e:
            raise AIExtractionError(f"failed to parse LLM response as JSON: {e}")
            
    except Exception as e:
        if isinstance(e, AIExtractionError):
            raise
        raise AIExtractionError(f"failed to extract receipt data: {e}")

def validate_json_with_schema(parsed_json: dict, schema: Type[BaseModel]) -> BaseModel:
    try:
        receipt = schema(**parsed_json)
        return receipt
    except ValidationError as e:
        raise SchemaValidationError(f"failed to validate json to schema: {e}") 
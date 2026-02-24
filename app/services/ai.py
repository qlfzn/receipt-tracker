import os
import json
from typing import Type, Dict
from dotenv import load_dotenv
from groq import Groq
from app.models.schemas import BankStatementResponse
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
    response_schema = BankStatementResponse.model_json_schema()

    example = """
    Example input:
    "
    Statement Date: 31/03/2024
    (Transaction)
    Date | Transaction Description | Transaction Amount |
    15/03 | TRANSFER FR A/C JOHN DOE* Friendly game payment | 450.00- |
    21/03 | TRANSFER TO A/C TOYYIBPAY SDN. BHD.* NPR4TADN040302414 MBB CT- | 380.00+ |
    25/03 | TRANSFER TO A/C CAROLYN BESSETE* Jersey payment | 100.00+ |
    "

    Example output:
    {
        "transactions": [
            {
                "date": "2024-03-15",
                "transaction": "TRANSFER FR A/C JOHN DOE",
                "amount": 450.00,
                "description": "Friendly game payment",
                "category": "transfer_in",
                "is_direct": true
            },
            {
                "date": "2024-03-21",
                "transaction": "TRANSFER TO A/C TOYYIBPAY SDN. BHD.",
                "amount": -380.00,
                "description": "NPR4TADN040302414 MBB CT",
                "category": "payment",
                "is_direct": false
            },
            {
                "date": "2024-03-25",
                "transaction": "TRANSFER TO A/C CAROLYN BESSETE",
                "amount": -100.00,
                "description": "Jersey payment",
                "category": "transfer_out",
                "is_direct": true
            }
        ]
    }
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"""
                    You are a Maybank bank statement data extraction expert. Extract all transactions from the statement text and return ONLY valid JSON matching the schema.
                    Schema to follow: {json.dumps(response_schema, indent=2)}

                    Rules:
                    - Return ONLY valid JSON, no markdown, no explanation
                    - Extract every transaction row — do not skip any
                    - Format all dates as YYYY-MM-DD, using the statement year when only day/month is given
                    - Use decimal numbers for amounts
                    - Inflows (TRANSFER FR A/C, credit entries) must have a positive amount
                    - Outflows (TRANSFER TO A/C, debit entries) must have a negative amount
                    - Strip reference codes and noise from the transaction name; keep only the counterparty name
                    - Put the human-readable payment purpose or reference code in the description field
                    - Set is_direct to false if the transaction involves a payment gateway (e.g. TOYYIBPAY, SHOPEE, GRAB, FPX, BILLPLZ); otherwise set is_direct to true
                    - Assign a category from: transfer_in, transfer_out
                    """,
                },
                {
                    "role": "user",
                    "content": f"{example}\n\nNow extract from this receipt:\n\n{parsed_text}",
                },
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

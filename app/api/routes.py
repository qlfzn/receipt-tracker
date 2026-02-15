from fastapi import APIRouter, File, UploadFile, HTTPException
from app.models.schemas import ParsedReceipt
from app.services.receipt_parser import parse_receipt, ReceiptParserError
from app.services.ai import generate_formatted_data, AIExtractionError


router = APIRouter()

@router.get("/")
def check_health():
    return "all good!"

@router.post("/receipts/upload", response_model=ParsedReceipt)
async def create_upload_file(file: UploadFile = File(...)):
    """
    Upload a PDF receipt and extract structured data.
    
    Returns structured receipt information including merchant, items, and totals.
    """
    if not file.filename.split(".")[1] == "pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )
    
    try:
        # Read and parse PDF
        contents = await file.read()
        extracted_text = parse_receipt(contents)
        
        # Extract structured data using AI
        receipt_data = generate_formatted_data(extracted_text)
        
        return receipt_data
        
    except ReceiptParserError as e:
        raise HTTPException(status_code=400, detail=f"error parsing file: {str(e)}")
    except AIExtractionError as e:
        raise HTTPException(status_code=422, detail=f"error extracting data: {str(e)}")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
    finally:
        await file.close()
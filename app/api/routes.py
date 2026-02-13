from fastapi import APIRouter, File, UploadFile, HTTPException
from app.models.schemas import ReceiptUploadResponse
from app.services.receipt_parser import parse_receipt, ReceiptParserError


router = APIRouter()

@router.get("/")
def check_health():
    return "all good!"

@router.post("/receipts/upload")
async def create_upload_file(file: UploadFile = File(...)):
    if not file.filename.lower().split(".")[1] == "pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF file supported"
        )
    try:
        contents = await file.read()
        extracted_text = parse_receipt(contents)

        return ReceiptUploadResponse(
            filename=file.filename,
            extracted_text=extracted_text,
            message=f"successfully processed {file.filename}"
        )
    except ReceiptParserError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"internal server error: {e}"
        )
    finally:
        await file.close()
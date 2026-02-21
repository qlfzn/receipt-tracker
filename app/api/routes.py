import io
from fastapi import APIRouter, File, UploadFile, HTTPException
from PIL import Image
from app.models.schemas import ParsedReceipt
from app.services.image_parser import get_text_from_image, ImageParseError
from app.services.ai import generate_formatted_data, validate_json_with_schema, AIExtractionError

router = APIRouter()

@router.get("/")
def read_root():
    """
    Base endpoint

    Returns:
        - Status message
    """
    return {"message": "all good!", "status": "200"}

@router.post("/receipts/upload", response_model=ParsedReceipt)
async def create_upload_file(file: UploadFile = File(...)):
    """
    Upload image of receipt and extract structured data.

    Returns:
        - ParsedReceipt: Structured receipt information
    """
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        extracted_text = get_text_from_image(image)
        
        # Extract structured data using AI
        parsed_data = generate_formatted_data(extracted_text)
        receipt_data = validate_json_with_schema(parsed_data, ParsedReceipt)
        
        return receipt_data
        
    except ImageParseError as e:
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
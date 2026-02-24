import fitz
import pytesseract
from PIL import Image

class PDFParserError(Exception):
    pass

def extract_text_from_pdf(contents: bytes) -> str:
    doc = fitz.open(stream=contents, filetype="pdf")
    full_text = ""

    for page in doc:
        # direct text extraction
        print("Attempting direct extraction...")
        page_content = page.get_text()
        text = page_content.strip() if isinstance(page_content, str) else ""

        if not text:
            # fallback to OCR
            print("Changing to OCR...")
            pix = page.get_pixmap(dpi=300)
            image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            text = pytesseract.image_to_string(image)

        full_text += text + "\n"

    return full_text

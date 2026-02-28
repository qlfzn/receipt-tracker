import fitz
import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes
import cv2
import numpy as np

class PDFParserError(Exception):
    pass

def extract_text_from_pdf(contents: bytes) -> str:
    pages = convert_from_bytes(contents)

    extracted_text = ""
    for page in pages:
        img_cv = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)

        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        
        text = pytesseract.image_to_string(thresh)
        extracted_text += text + "\n"
        
    return extracted_text
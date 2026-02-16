import pytesseract

class ImageParseError(Exception):
    pass

def get_text_from_image(image_content) -> str:
    try:
        text = pytesseract.image_to_string(image=image_content)
        return text 
    except Exception as e:
        raise ImageParseError(f"failed to extract from image: {e}")
from pypdf import PdfReader
from io import BytesIO

class ReceiptParserError(Exception):
    pass

def parse_receipt(file_content: bytes) -> str:
    # only expect PDF
    try:
        pdf_file = BytesIO(file_content)
        reader = PdfReader(pdf_file)

        # check no. of pages
        if len(reader.pages) < 1:
            raise ReceiptParserError("PDF has no pages")

        # extract text from all pages
        text_content = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_content.append(text)
        return "\n".join(text_content)

    except Exception as e:
        raise ReceiptParserError(f"Failed to read file: {e}")
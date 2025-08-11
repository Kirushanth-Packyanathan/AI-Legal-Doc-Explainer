import pdfplumber
import pytesseract
from pdf2image import convert_from_path
import tempfile


def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    if text.strip():
        return text

    # If no text found → use OCR
    return ocr_pdf(file_path)


def ocr_pdf(file_path: str) -> str:
    text = ""
    with tempfile.TemporaryDirectory() as temp_dir:
        images = convert_from_path(file_path, output_folder=temp_dir)
        for image in images:
            text += pytesseract.image_to_string(image) + "\n"
    return text

import fitz  # PyMuPDF
from PIL import Image
from docx import Document
import pytesseract

import platform
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(file_path):
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image)
    return text

def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    pdf = fitz.open(file_path)

    for page in pdf:
        blocks = page.get_text("blocks")  # get text in blocks/paragraphs
        for block in blocks:
            if block[6] == 0:  # text block (not image)
                text += block[4].strip() + "\n\n"

    pdf.close()
    return text.strip()


def extract_text_from_docx(file_path: str) -> str:
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text


def extract_text_from_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def extract_text(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)

    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)

    elif file_path.endswith(".txt"):
        return extract_text_from_txt(file_path)
    
    elif file_path.endswith((".png", ".jpg", ".jpeg")):
        return extract_text_from_image(file_path)

    else:
        raise ValueError("Unsupported file type")
        

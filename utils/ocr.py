import pytesseract
import cv2
from pdf2image import convert_from_path
import numpy as np
import logging
import re

# ✅ Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ✅ Poppler path
POPPLER_PATH = r"C:\Program Files\poppler-23.11.0\Library\bin"


def preprocess_image(img):
    """Improve OCR accuracy for documents"""
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    gray = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 2
    )
    return gray


# Dictionary of common OCR typos to fix
OCR_FIXES = {
    r"\bCurreni[eé]y\b": "Currency",
    r"\bAddreza\b": "Address",
    r"\bAddrese\b": "Address",
    r"\bBenefl[^\s]*lary\b": "Beneficiary",
    r"\bBendliciary\b": "Beneficiary",
    r"\bRemiltter\b": "Remitter",
    r"\bApplicarit\b": "Applicant",
    r"etfact": "effect",
    r"ramittance": "remittance",
    r"euuto fos": "",  # garbage, remove
    r"\*Terorist DB checked": "",  # remove unwanted
    r"\| \|": "",  # remove empty pipes
}


def format_text(text):
    """Normalize OCR text with line breaks, fix typos, and enforce keywords"""
    # normalize line breaks
    text = text.replace('\r\n', '\n').replace('\r', '\n')

    # remove extra spaces
    text = re.sub(r"[ \t]+", " ", text)

    # apply OCR typo fixes
    for pattern, replacement in OCR_FIXES.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    # split lines and keep non-empty lines
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    formatted_text = "\n".join(lines)

    # keywords to start on a new line
    keywords = [
        "REMITTANCE APPLICATION", "Name of Beneficiary", "Address",
        "Account No", "Currency", "Amount", "USD", "INTERNAL TRANSFER",
        "BNP PARIBAS", "Swift", "Bank", "Date", "Message or Instructions to Beneficiary"
    ]

    for kw in keywords:
        formatted_text = re.sub(rf"(?<!\n)({re.escape(kw)})", r"\n\1", formatted_text)

    # remove multiple consecutive newlines
    formatted_text = re.sub(r"\n+", "\n", formatted_text)

    return formatted_text.strip()


def run_ocr(pdf_path):
    """Run OCR on a PDF and return cleaned text"""
    text = ""

    try:
        pages = convert_from_path(
            pdf_path,
            dpi=300,
            poppler_path=POPPLER_PATH
        )

        for page in pages:
            img = np.array(page)
            processed = preprocess_image(img)

            page_text = pytesseract.image_to_string(
                processed,
                config="--oem 3 --psm 6"  # single uniform block of text
            )

            text += page_text + "\n"

    except Exception as e:
        logging.error(f"OCR failed for {pdf_path}: {e}")

    return format_text(text)

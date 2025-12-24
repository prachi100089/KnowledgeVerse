import re
from datetime import datetime


def extract_invoice_fields(text, filename):
    invoice_no = ""
    invoice_date = ""
    currency = ""
    grand_total = ""

    name = filename.replace(".pdf", "").upper()

    # ---------------------------
    # 1️⃣ DATE — YYYYMMDD (highest priority)
    # ---------------------------
    m = re.search(r"(20\d{2})(\d{2})(\d{2})", name)
    if m:
        y, mth, d = m.groups()
        invoice_date = datetime.strptime(
            f"{d}-{mth}-{y}", "%d-%m-%Y"
        ).strftime("%d-%b-%Y")

    # ---------------------------
    # 2️⃣ DATE — 17JUL20 format
    # ---------------------------
    if not invoice_date:
        m = re.search(r"(\d{2})([A-Z]{3})(\d{2})", name)
        if m:
            d, mon, y = m.groups()
            invoice_date = f"{d}-{mon.capitalize()}-20{y}"

    # ---------------------------
    # 3️⃣ INVOICE NUMBER
    # ---------------------------
    clean_name = re.sub(r"[^\w]", "", name)

    if clean_name.isdigit():
        invoice_no = clean_name

    if not invoice_no:
        m = re.search(r"\d{2}[A-Z]{3}\d{2}", name)
        if m:
            invoice_no = m.group(0)

    if not invoice_no:
        m = re.search(r"Invoice\s*(No|#|Number)[:\-]?\s*([A-Za-z0-9\-]+)", text, re.I)
        if m:
            invoice_no = m.group(2)

    # ---------------------------
    # 4️⃣ TOTAL + CURRENCY (TEXT)
    # ---------------------------
    total_patterns = [
        r"(USD|INR|EUR|US\$)\s*([\d,]+\.\d{2})",
        r"([\d,]+\.\d{2})\s*(USD|INR|EUR|US\$)"
    ]

    for p in total_patterns:
        m = re.search(p, text)
        if m:
            if m.group(1).replace(",", "").replace(".", "").isdigit():
                grand_total = m.group(1)
                currency = m.group(2)
            else:
                currency = m.group(1)
                grand_total = m.group(2)
            break

    # ---------------------------
    # 5️⃣ FALLBACK: AMOUNT FROM FILENAME
    # ---------------------------
    if not grand_total:
        m = re.search(r"(USD|INR|EUR|US\$)\s*([\d,]+\.\d{2})", name)
        if m:
            currency = m.group(1)
            grand_total = m.group(2)

    # Normalize currency
    if currency == "US$":
        currency = "USD"

    return {
        "invoice_id": filename,
        "invoice_no": invoice_no,
        "invoice_date": invoice_date,
        "currency": currency,
        "grand_total": grand_total
    }

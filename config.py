# config.py

DATE_REGEX = r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b"
INVOICE_NO_REGEX = r"(Invoice\s*(No|#|Number)[:\s]*)(\S+)"
TOTAL_KEYWORDS = ["grand total", "total due", "amount payable"]
CURRENCY_SYMBOLS = ["₹", "$", "€", "INR", "USD", "EUR"]

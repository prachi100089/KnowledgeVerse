import os
import argparse
import logging

from utils.ocr import run_ocr
from utils.parser import extract_invoice_fields
from utils.exporter import export_csv_json

logging.basicConfig(level=logging.INFO)


def main():
    parser = argparse.ArgumentParser(description="PDF Invoice OCR → CSV/JSON")
    parser.add_argument("--in_dir", required=True, help="Input PDF directory")
    parser.add_argument("--out_csv", required=True, help="Output CSV file")
    parser.add_argument("--out_json", required=True, help="Raw OCR JSON directory")
    args = parser.parse_args()

    in_dir = os.path.abspath(args.in_dir)
    out_csv = os.path.abspath(args.out_csv)
    out_json = os.path.abspath(args.out_json)

    rows = []
    raw_texts = {}

    for file in sorted(os.listdir(in_dir)):
        if not file.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(in_dir, file)
        logging.info(f"Processing: {file}")

        text = run_ocr(pdf_path)

        if not text.strip():
            logging.warning(f"OCR returned empty text for {file}")

        raw_texts[file] = text

        data = extract_invoice_fields(text, file)
        rows.append(data)

    export_csv_json(rows, raw_texts, out_csv, out_json)
    logging.info("✅ Processing complete")


if __name__ == "__main__":
    main()

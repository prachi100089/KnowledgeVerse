import pandas as pd
import json
import os


def export_csv_json(rows, raw_texts, out_csv, out_json_dir):
    os.makedirs(out_json_dir, exist_ok=True)

    # ---------------------------
    # 1️⃣ Normalize CSV columns
    # ---------------------------
    all_keys = set()
    for row in rows:
        all_keys.update(row.keys())

    normalized_rows = []
    for row in rows:
        normalized_rows.append({k: row.get(k, "") for k in all_keys})

    df = pd.DataFrame(normalized_rows)
    df.to_csv(out_csv, index=False)

    # ---------------------------
    # 2️⃣ Raw OCR JSON (clean filenames)
    # ---------------------------
    for fname, text in raw_texts.items():
        base = os.path.splitext(fname)[0]

        payload = {
            "filename": fname,
            "text_length": len(text),
            "text": text
        }

        with open(
            os.path.join(out_json_dir, f"{base}.json"),
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(payload, f, indent=2)

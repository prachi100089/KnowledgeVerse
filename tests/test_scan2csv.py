import os
import csv
import subprocess
import pytest

# Paths
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SAMPLE_INPUT = os.path.join(REPO_ROOT, "sample_input")
SAMPLE_OUTPUT = os.path.join(REPO_ROOT, "sample_output")
HEADER_CSV = os.path.join(SAMPLE_OUTPUT, "invoices_header.csv")
RAW_JSON_DIR = os.path.join(SAMPLE_OUTPUT, "raw")


def test_scan2csv_runs():
    """Run the CLI script and ensure it completes without error"""
    cmd = [
        "python",
        os.path.join(REPO_ROOT, "scan2csv.py"),
        "--in_dir", SAMPLE_INPUT,
        "--out_csv", HEADER_CSV,
        "--out_json", RAW_JSON_DIR
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
    assert result.returncode == 0


def test_header_csv_exists_and_not_empty():
    """Check that header CSV exists and has at least one row (excluding header)"""
    assert os.path.exists(HEADER_CSV), "Header CSV not found"
    with open(HEADER_CSV, newline="", encoding="utf-8") as f:
        reader = list(csv.reader(f))
        assert len(reader) > 1, "Header CSV is empty"


def test_raw_json_files_exist():
    """Check that raw JSON files were generated for each input PDF"""
    input_files = [f for f in os.listdir(SAMPLE_INPUT) if f.lower().endswith(".pdf")]
    json_files = [f for f in os.listdir(RAW_JSON_DIR) if f.endswith(".json")]
    for pdf in input_files:
        json_name = pdf.replace(".pdf", ".json")
        assert json_name in json_files, f"Raw JSON for {pdf} not found"

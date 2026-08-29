import csv
import os
from datasets import load_dataset

dir = "/home/akkim7/string_datasets/"
GIGABYTE = 1073741824
RAW_CSV = dir + "stackoverflow_raw.csv"
OUTPUT_CSV = dir + "stackoverflow.csv"


# ── Step 1: Fetch question titles from HuggingFace dataset ────────────────

def fetch_stackoverflow_titles(out_path):
    """
    Downloads the pacovaldez/stackoverflow-questions dataset from HuggingFace
    and writes all question titles to a raw CSV.
    """
    os.makedirs(dir, exist_ok=True)

    print("Loading dataset from HuggingFace (this may take a while)...")
    dataset = load_dataset("pacovaldez/stackoverflow-questions", split="train")

    total_fetched = 0
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["title"])
        for row in dataset:
            title = row["title"].strip()
            if title:
                writer.writerow([title])
                total_fetched += 1
                if total_fetched % 100000 == 0:
                    print(f"Fetched {total_fetched:,} titles...")

    print(f"Raw fetch complete: {total_fetched:,} titles → {out_path}")
    return total_fetched


# ── Step 2: Expand raw CSV to 10 GB (same loop as other scripts) ──────────

def process_csv(input_filename, output_filename):
    ifobj = open(input_filename, "r", encoding="utf-8")
    ifcsvobj = csv.reader(ifobj)
    ofname = output_filename
    ofobj = open(ofname, "w", encoding="utf-8")
    ofcsvobj = csv.writer(ofobj)

    inputrows = list(ifcsvobj)
    print(f"Loaded {len(inputrows):,} rows from raw CSV")

    total_bytes = 0
    total_len = 10 * GIGABYTE
    gb_written = 0
    row_idx = 0

    while total_bytes < total_len and row_idx < len(inputrows):
        message = inputrows[row_idx][0]
        row_idx += 1
        if row_idx == len(inputrows):
            row_idx = 0
        total_bytes += len(message)
        ofcsvobj.writerow([message.replace("\n", "")])
        current_gb = total_bytes // GIGABYTE
        if current_gb > gb_written:
            gb_written = current_gb
            print(f"Written {gb_written} GB of data ({total_bytes:,} bytes)")

    ifobj.close()
    ofobj.close()
    print("Data has been generated")


# ── Main ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Step 1: Fetching StackOverflow question titles ===")
    n = fetch_stackoverflow_titles(RAW_CSV)

    if n == 0:
        print("ERROR: No titles fetched. Check network/dataset and retry.")
        exit(1)

    print("\n=== Step 2: Generating 10 GB dataset ===")
    process_csv(RAW_CSV, OUTPUT_CSV)
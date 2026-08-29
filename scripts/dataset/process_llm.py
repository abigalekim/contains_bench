import csv
import os
from datasets import load_dataset

dir = "/home/akkim7/string_datasets/"
GIGABYTE = 1073741824
RAW_CSV = dir + "llm_prompts_raw.csv"
OUTPUT_CSV = dir + "llm_prompts.csv"


# ── Step 1: Fetch prompts from HuggingFace ────────────────────────────────

def fetch_prompts(out_path):
    os.makedirs(dir, exist_ok=True)

    print("Loading codesagar/malicious-llm-prompts from HuggingFace...")
    dataset = load_dataset("codesagar/malicious-llm-prompts")

    total_fetched = 0
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["prompt"])
        for split in dataset.values():
            for row in split:
                prompt = row["prompt"].strip() if row.get("prompt") else ""
                if prompt:
                    writer.writerow([prompt])
                    total_fetched += 1

    print(f"Raw fetch complete: {total_fetched:,} prompts → {out_path}")
    return total_fetched


# ── Step 2: Expand raw CSV to 10 GB (same loop as other scripts) ──────────

def process_csv(input_filename, output_filename):
    import sys
    csv.field_size_limit(sys.maxsize)

    ifobj = open(input_filename, "r", encoding="utf-8")
    ifcsvobj = csv.reader(ifobj)
    ofobj = open(output_filename, "w", encoding="utf-8")
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
    print("=== Step 1: Fetching LLM prompts ===")
    n = fetch_prompts(RAW_CSV)

    if n == 0:
        print("ERROR: No prompts fetched.")
        exit(1)

    print("\n=== Step 2: Generating 10 GB dataset ===")
    process_csv(RAW_CSV, OUTPUT_CSV)
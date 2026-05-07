import csv
import os
import sys
import json
from datasets import load_dataset

dir = "/home/akkim7/string_datasets/"
GIGABYTE = 1073741824
RAW_CSV = dir + "lmsys_chat_raw.csv"
OUTPUT_CSV = dir + "lmsys_chat.csv"


# ── Step 1: Fetch all user turns from every conversation ─────────────────
# NOTE: You must first accept the dataset license at:
#   https://huggingface.co/datasets/lmsys/lmsys-chat-1m
# Then run: huggingface-cli login
# before this script will work.

def fetch_prompts(out_path):
    os.makedirs(dir, exist_ok=True)

    print("Loading lmsys/lmsys-chat-1m from HuggingFace...")
    dataset = load_dataset("lmsys/lmsys-chat-1m", split="train")

    total_fetched = 0
    total_skipped = 0

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["prompt"])

        for row in dataset:
            # Filter to English only
            if row.get("language") != "English":
                total_skipped += 1
                continue

            # conversation is a list of {"role": ..., "content": ...} dicts
            conversation = row.get("conversation", [])
            if not conversation:
                total_skipped += 1
                continue

            # Extract all user turns
            for turn in conversation:
                if turn.get("role") == "user":
                    content = turn.get("content", "").strip()
                    if content:
                        writer.writerow([content])
                        total_fetched += 1

            if total_fetched % 50000 == 0:
                print(f"Fetched {total_fetched:,} turns (skipped {total_skipped:,} non-English conversations)...")

    print(f"Raw fetch complete: {total_fetched:,} user turns → {out_path}")
    return total_fetched


# ── Step 2: Expand raw CSV to 10 GB (same loop as other scripts) ──────────

def process_csv(input_filename, output_filename):
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
    print("=== Step 1: Fetching LMSYS Chat prompts ===")
    n = fetch_prompts(RAW_CSV)

    if n == 0:
        print("ERROR: No prompts fetched. Have you accepted the license and run `huggingface-cli login`?")
        exit(1)

    print("\n=== Step 2: Generating 10 GB dataset ===")
    process_csv(RAW_CSV, OUTPUT_CSV)
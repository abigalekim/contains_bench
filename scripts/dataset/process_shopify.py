import csv
import re
import os
from datasets import load_dataset

dir = "/home/akkim7/string_datasets/"
GIGABYTE = 1073741824
RAW_CSV = dir + "shopify_raw.csv"
OUTPUT_CSV = dir + "shopify.csv"

ASCII_ONLY = re.compile(r'[^\x00-\x7F]')


def is_english(text):
    # Reject if more than 5% of characters are non-ASCII
    non_ascii = len(ASCII_ONLY.findall(text))
    return non_ascii / max(len(text), 1) < 0.05


def fetch_shopify_titles(out_path):
    os.makedirs(dir, exist_ok=True)

    print("Loading Shopify/product-catalogue from HuggingFace...")
    dataset = load_dataset("Shopify/product-catalogue")

    total_fetched = 0
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["product_title"])
        for split in dataset.values():
            for row in split:
                title = row["product_title"].strip()
                if title and is_english(title):
                    writer.writerow([title])
                    total_fetched += 1
                    if total_fetched % 10000 == 0:
                        print(f"Fetched {total_fetched:,} titles...")

    print(f"Raw fetch complete: {total_fetched:,} titles → {out_path}")
    return total_fetched


def process_csv(input_filename, output_filename):
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


if __name__ == "__main__":
    print("=== Step 1: Fetching Shopify product titles ===")
    n = fetch_shopify_titles(RAW_CSV)

    if n == 0:
        print("ERROR: No titles fetched.")
        exit(1)

    print("\n=== Step 2: Generating 10 GB dataset ===")
    process_csv(RAW_CSV, OUTPUT_CSV)
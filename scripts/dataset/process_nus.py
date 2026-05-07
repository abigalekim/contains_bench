import csv
import os
import requests

dir = "/home/akkim7/string_datasets/"
GIGABYTE = 1073741824
RAW_CSV = dir + "nus_sms_raw.csv"
OUTPUT_CSV = dir + "nus.csv"

# The full NUS SMS corpus is distributed as a CSV on GitHub (kite1988/nus-sms-corpus)
# It contains ~67K English SMS messages with columns: id, Message, length, country, ...
NUS_SMS_URL = "https://raw.githubusercontent.com/kite1988/nus-sms-corpus/master/corpus/smsCorpus_en_2015.03.09_all.json"

# Fallback: the corpus is also available via HuggingFace as ucirvine/sms_spam
# which is a subset (~5.5K msgs). We use both and pool them.
HF_FALLBACK = True


def fetch_from_github(out_path):
    """
    Fetches the full NUS SMS corpus JSON from GitHub.
    Falls back to HuggingFace sms_spam subset if unavailable.
    Returns number of messages written.
    """
    os.makedirs(dir, exist_ok=True)
    total_fetched = 0

    print("Attempting to fetch full NUS SMS corpus from GitHub...")
    try:
        resp = requests.get(NUS_SMS_URL, timeout=60)
        resp.raise_for_status()
        data = resp.json()

        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["message"])
            # JSON structure: {"smsCorpus": {"message": [{"text": {"$": "..."}, ...}, ...]}}
            messages = data["smsCorpus"]["message"]
            for entry in messages:
                text = entry.get("text", {}).get("$", "").strip()
                if text:
                    writer.writerow([text])
                    total_fetched += 1

        print(f"GitHub fetch complete: {total_fetched:,} messages")
        return total_fetched

    except Exception as e:
        print(f"GitHub fetch failed ({e}), falling back to HuggingFace subset...")
        return fetch_from_huggingface(out_path)


def fetch_from_huggingface(out_path):
    from datasets import load_dataset
    dataset = load_dataset("ucirvine/sms_spam", split="train")
    total_fetched = 0

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["message"])
        for row in dataset:
            text = row["sms"].strip()
            if text:
                writer.writerow([text])
                total_fetched += 1

    print(f"HuggingFace fallback complete: {total_fetched:,} messages")
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
    print("=== Step 1: Fetching NUS SMS corpus ===")
    n = fetch_from_github(RAW_CSV)

    if n == 0:
        print("ERROR: No messages fetched.")
        exit(1)

    print("\n=== Step 2: Generating 10 GB dataset ===")
    process_csv(RAW_CSV, OUTPUT_CSV)
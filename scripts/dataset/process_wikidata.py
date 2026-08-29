import csv
import requests
import time
import os

dir = "/home/akkim7/string_datasets/"
GIGABYTE = 1073741824
RAW_CSV = dir + "wikidata_raw.csv"
OUTPUT_CSV = dir + "wikidata.csv"


# ── Step 1: Fetch short descriptions from Wikidata SPARQL ──────────────────

def fetch_wikidata_descriptions(out_path, batch_size=10000, max_items=500000):
    """
    Queries the Wikidata SPARQL endpoint for English short descriptions
    (schema:description) and writes them to a raw CSV.
    Paginates with LIMIT/OFFSET until max_items are collected or results dry up.
    """
    endpoint = "https://query.wikidata.org/sparql"
    headers = {
        "Accept": "application/sparql-results+json",
        "User-Agent": "wikidata-desc-fetcher/1.0 (research benchmark dataset)"
    }

    os.makedirs(dir, exist_ok=True)
    total_fetched = 0
    offset = 0

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["description"])

        while total_fetched < max_items:
            query = f"""
SELECT ?desc WHERE {{
  ?item schema:description ?desc .
  FILTER(LANG(?desc) = "en")
  FILTER(STRLEN(?desc) > 0)
}}
LIMIT {batch_size}
OFFSET {offset}
"""
            try:
                resp = requests.get(
                    endpoint,
                    params={"query": query, "format": "json"},
                    headers=headers,
                    timeout=120
                )
                resp.raise_for_status()
                results = resp.json()["results"]["bindings"]
            except Exception as e:
                print(f"Error at offset {offset}: {e}. Retrying in 10s...")
                time.sleep(10)
                continue

            if not results:
                print(f"No more results at offset {offset}. Done fetching.")
                break

            for row in results:
                desc = row["desc"]["value"].strip()
                if desc:
                    writer.writerow([desc])
                    total_fetched += 1

            print(f"Fetched {total_fetched:,} descriptions (offset={offset})")
            offset += batch_size

            # Be polite to the public endpoint
            time.sleep(1)

    print(f"Raw fetch complete: {total_fetched:,} descriptions → {out_path}")
    return total_fetched


# ── Step 2: Expand raw CSV to 10 GB (same loop as other scripts) ───────────

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


# ── Main ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Step 1: Fetching Wikidata descriptions ===")
    n = fetch_wikidata_descriptions(RAW_CSV, batch_size=10000, max_items=500000)

    if n == 0:
        print("ERROR: No descriptions fetched. Check network/endpoint and retry.")
        exit(1)

    print("\n=== Step 2: Generating 10 GB dataset ===")
    process_csv(RAW_CSV, OUTPUT_CSV)
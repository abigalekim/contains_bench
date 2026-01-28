import gzip
from warcio.archiveiterator import ArchiveIterator
import csv
import matplotlib.pyplot as plt
import sys

# Install warcio first: pip install warcio

# Update this to match your downloaded WARC file name
# It will be something like: CC-MAIN-20251117134315-20251117164315-00000.warc.gz
input_file = "/mnt/wiscdb/abigale/CC-MAIN-20251106200718-20251106230718-00000.warc.gz"  # Update this!
output_file = "/mnt/wiscdb/abigale/string_dataset_csvs/common_crawl_urls.csv"
lengths = []
urls = []

GIGABYTE = 1073741824

print("Processing WARC file...")
print("This may take several minutes for a 1GB file...")

try:
    with gzip.open(input_file, 'rb') as stream:
        for idx, record in enumerate(ArchiveIterator(stream)):
            if record.rec_type in ['response', 'request']:
                url = record.rec_headers.get_header('WARC-Target-URI')
                if url:
                    urls.append(url)
                    lengths.append(len(url))
                    
                    if len(urls) % 10000 == 0:
                        print(f"Processed {len(urls)} URLs...")
                        
except Exception as e:
    print(f"Error processing WARC: {e}")
    sys.exit(1)

print(f"\n{'='*60}")
print(f"Total URLs: {len(lengths)}")
print(f"Average length: {sum(lengths)/len(lengths):.2f}")
print(f"Min length: {min(lengths)}")
print(f"Max length: {max(lengths)}")
print(f"Median length: {sorted(lengths)[len(lengths)//2]}")

sorted_lengths = sorted(lengths)
print(f"\nPercentiles:")
print(f"  10th: {sorted_lengths[int(len(sorted_lengths) * 0.1)]}")
print(f"  25th: {sorted_lengths[int(len(sorted_lengths) * 0.25)]}")
print(f"  50th: {sorted_lengths[int(len(sorted_lengths) * 0.5)]}")
print(f"  75th: {sorted_lengths[int(len(sorted_lengths) * 0.75)]}")
print(f"  90th: {sorted_lengths[int(len(sorted_lengths) * 0.9)]}")
print(f"  95th: {sorted_lengths[int(len(sorted_lengths) * 0.95)]}")
print(f"  99th: {sorted_lengths[int(len(sorted_lengths) * 0.99)]}")

print(f"\nDistribution:")
print(f"  Strings < 32 bytes: {sum(1 for l in lengths if l < 32)} ({sum(1 for l in lengths if l < 32) / len(lengths) * 100:.2f}%)")
print(f"  Strings 32-128 bytes: {sum(1 for l in lengths if 32 <= l < 128)} ({sum(1 for l in lengths if 32 <= l < 128) / len(lengths) * 100:.2f}%)")
print(f"  Strings > 8192 bytes: {sum(1 for l in lengths if l > 8192)} ({sum(1 for l in lengths if l > 8192) / len(lengths) * 100:.2f}%)")
print(f"{'='*60}\n")

# Write to CSV with 5GB limit
print("Writing to CSV...")
with open(output_file, "w", encoding="utf-8", newline='') as f_out:
    writer = csv.writer(f_out)
    total_bytes = 0
    total_len = 5 * GIGABYTE
    gb_written = 0
    row_idx = 0
    
    while total_bytes < total_len:
        url = urls[row_idx]
        row_idx += 1
        if row_idx == len(urls):
            row_idx = 0  # Loop back to beginning
        
        total_bytes += len(url)
        writer.writerow([url])
        
        current_gb = total_bytes // GIGABYTE
        if current_gb > gb_written:
            gb_written = current_gb
            print(f"Written {gb_written} GB of data ({total_bytes:,} bytes)")

print("Done! CSV file written")

# Plot histogram
print("Creating histograms...")
plt.figure(figsize=(12, 6))
plt.hist(lengths, bins=100, edgecolor='black', alpha=0.7)
plt.xlabel('URL Length (characters)')
plt.ylabel('Frequency')
plt.title('Distribution of Common Crawl URL Lengths')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('commoncrawl_urls_histogram.png', dpi=300)

plt.figure(figsize=(12, 6))
plt.hist(lengths, bins=100, edgecolor='black', alpha=0.7)
plt.xlabel('URL Length (characters)')
plt.ylabel('Frequency (log scale)')
plt.title('Distribution of Common Crawl URL Lengths (Log Scale)')
plt.yscale('log')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('commoncrawl_urls_histogram_log.png', dpi=300)
plt.show()

print("\nHistograms saved as 'commoncrawl_urls_histogram.png' and 'commoncrawl_urls_histogram_log.png'")
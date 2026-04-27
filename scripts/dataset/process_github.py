import csv
import matplotlib.pyplot as plt
import sys

csv.field_size_limit(sys.maxsize)

input_file = "/home/akkim7/.cache/kagglehub/datasets/dhruvildave/github-commit-messages-dataset/versions/3/full.csv"
output_file = "/home/akkim7/string_datasets/github_commits.csv"
lengths = []

GIGABYTE = 1073741824

# First pass: collect all commit messages and their lengths
commit_messages = []
with open(input_file, 'r', encoding='utf-8') as fp:
    reader = csv.DictReader(fp)
    for row in reader:
        message = row["message"]  # The commit message column
        commit_messages.append(message)
        lengths.append(len(message))

# Print some statistics
print(f"Total commits: {len(lengths)}")
print(f"Average length: {sum(lengths)/len(lengths):.2f}")
print(f"Min length: {min(lengths)}")
print(f"Max length: {max(lengths)}")
print(f"Median length: {sorted(lengths)[len(lengths)//2]}")

# Print percentiles to see distribution
sorted_lengths = sorted(lengths)
print(f"90th percentile: {sorted_lengths[int(len(sorted_lengths) * 0.9)]}")
print(f"95th percentile: {sorted_lengths[int(len(sorted_lengths) * 0.95)]}")
print(f"99th percentile: {sorted_lengths[int(len(sorted_lengths) * 0.99)]}")
print(f"Strings < 32 bytes: {sum(1 for l in lengths if l < 32) / len(lengths) * 100:.2f}%")
print(f"Strings > 8192 bytes: {sum(1 for l in lengths if l > 8192)}")

## Write to CSV with 2GB upper bound
with open(output_file, "w", encoding="utf-8", newline='') as f_out:
    writer = csv.writer(f_out)
    total_bytes = 0
    total_len = 10 * GIGABYTE
    gb_written = 0
    row_idx = 0
    
    while total_bytes < total_len:
        message = commit_messages[row_idx]
        row_idx += 1
        if row_idx == len(commit_messages):
            row_idx = 0
        
        total_bytes += len(message)
        writer.writerow([message.replace("\n", " ")])  # Replace newlines with spaces
        
        current_gb = total_bytes // GIGABYTE
        if current_gb > gb_written:
            gb_written = current_gb
            print(f"Written {gb_written} GB of data ({total_bytes:,} bytes)")

print("Done! CSV file written")

## Plot histogram
#plt.figure(figsize=(12, 6))
#plt.hist(lengths, bins=100, edgecolor='black', alpha=0.7)
#plt.xlabel('Commit Message Length (characters)')
#plt.ylabel('Frequency')
#plt.title('Distribution of GitHub Commit Message Lengths')
#plt.grid(True, alpha=0.3)
#
#plt.tight_layout()
#plt.savefig('github_commits_histogram.png', dpi=300)
#
## Also plot with log scale to see the long tail better
#plt.figure(figsize=(12, 6))
#plt.hist(lengths, bins=100, edgecolor='black', alpha=0.7)
#plt.xlabel('Commit Message Length (characters)')
#plt.ylabel('Frequency (log scale)')
#plt.title('Distribution of GitHub Commit Message Lengths (Log Scale)')
#plt.yscale('log')
#plt.grid(True, alpha=0.3)
#
#plt.tight_layout()
#plt.savefig('github_commits_histogram_log.png', dpi=300)
#plt.show()
#
#print("\nHistograms saved as 'github_commits_histogram.png' and 'github_commits_histogram_log.png'")
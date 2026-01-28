import csv
import matplotlib.pyplot as plt
import re
import sys

csv.field_size_limit(sys.maxsize)

# Loghub datasets: https://github.com/logpai/loghub
# Or use your own system logs from /var/log/syslog

# Example with a downloadable syslog-style dataset
# You can download from: https://zenodo.org/record/3227177 (Hadoop logs)
# Or any of the Loghub datasets

input_file = "/path/to/syslog/or/application.log"  # Update this path
output_file = "/mnt/wiscdb/abigale/string_dataset_csvs/syslog_messages.csv"
lengths = []
messages = []

GIGABYTE = 1073741824

# Process log file - extract just the message content
with open(input_file, 'r', encoding='utf-8', errors='ignore') as fp:
    for line in fp:
        # Strip timestamp and log level, keep just the message
        # Adjust regex based on your log format
        # Example: "2024-01-01 12:00:00 INFO This is the message"
        match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \w+ (.*)', line)
        if match:
            message = match.group(1).strip()
        else:
            message = line.strip()
        
        if message:
            messages.append(message)
            lengths.append(len(message))

# Print statistics
print(f"Total log messages: {len(lengths)}")
print(f"Average length: {sum(lengths)/len(lengths):.2f}")
print(f"Min length: {min(lengths)}")
print(f"Max length: {max(lengths)}")
print(f"Median length: {sorted(lengths)[len(lengths)//2]}")

sorted_lengths = sorted(lengths)
print(f"90th percentile: {sorted_lengths[int(len(sorted_lengths) * 0.9)]}")
print(f"95th percentile: {sorted_lengths[int(len(sorted_lengths) * 0.95)]}")
print(f"99th percentile: {sorted_lengths[int(len(sorted_lengths) * 0.99)]}")
print(f"Strings < 32 bytes: {sum(1 for l in lengths if l < 32) / len(lengths) * 100:.2f}%")
print(f"Strings > 8192 bytes: {sum(1 for l in lengths if l > 8192)}")

# Write to CSV
#with open(output_file, "w", encoding="utf-8", newline='') as f_out:
#    writer = csv.writer(f_out)
#    total_bytes = 0
#    total_len = 5 * GIGABYTE
#    gb_written = 0
#    row_idx = 0
#    
#    while total_bytes < total_len:
#        message = messages[row_idx]
#        row_idx += 1
#        if row_idx == len(messages):
#            row_idx = 0
#        
#        total_bytes += len(message)
#        writer.writerow([message.replace("\n", " ")])
#        
#        current_gb = total_bytes // GIGABYTE
#        if current_gb > gb_written:
#            gb_written = current_gb
#            print(f"Written {gb_written} GB of data ({total_bytes:,} bytes)")
#
#print("Done! CSV file written")
#
## Plot histogram
#plt.figure(figsize=(12, 6))
#plt.hist(lengths, bins=100, edgecolor='black', alpha=0.7)
#plt.xlabel('Message Length (characters)')
#plt.ylabel('Frequency')
#plt.title('Distribution of Log Message Lengths')
#plt.grid(True, alpha=0.3)
#plt.tight_layout()
#plt.savefig('syslog_histogram.png', dpi=300)
#
#plt.figure(figsize=(12, 6))
#plt.hist(lengths, bins=100, edgecolor='black', alpha=0.7)
#plt.xlabel('Message Length (characters)')
#plt.ylabel('Frequency (log scale)')
#plt.title('Distribution of Log Message Lengths (Log Scale)')
#plt.yscale('log')
#plt.grid(True, alpha=0.3)
#plt.tight_layout()
#plt.savefig('syslog_histogram_log.png', dpi=300)
#plt.show()
#
#print("\nHistograms saved")
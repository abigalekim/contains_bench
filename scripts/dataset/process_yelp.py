import json
import csv
import matplotlib.pyplot as plt

# Yelp dataset is typically in JSON format (one JSON object per line)
file = "/home/akkim7/yelp_academic_dataset_review.json"
output_file = "/home/akkim7/string_datasets/yelp_reviews.csv"
lengths = []

GIGABYTE = 1073741824

# First pass: collect all reviews and their lengths
reviews = []
with open(file, 'r', encoding='utf-8') as fp:
    for line in fp:
        review_data = json.loads(line.strip())
        text = review_data["text"]  # The review text field
        reviews.append(text)
        lengths.append(len(text))

# Print some statistics
print(f"Total reviews: {len(lengths)}")
print(f"Average length: {sum(lengths)/len(lengths):.2f}")
print(f"Min length: {min(lengths)}")
print(f"Max length: {max(lengths)}")
print(f"Median length: {sorted(lengths)[len(lengths)//2]}")

# Write to CSV with 5GB upper bound
with open(output_file, "w", encoding="utf-8", newline='') as f_out:
    writer = csv.writer(f_out)
    total_bytes = 0
    total_len = 3 * GIGABYTE
    gb_written = 0
    row_idx = 0
    
    while total_bytes < total_len:
        message = reviews[row_idx]
        row_idx += 1
        if row_idx == len(reviews):
            row_idx = 0
        
        total_bytes += len(message)
        writer.writerow([message.replace("\n", "")])
        
        current_gb = total_bytes // GIGABYTE
        if current_gb > gb_written:
            gb_written = current_gb
            print(f"Written {gb_written} GB of data ({total_bytes:,} bytes)")

print("Done! CSV file written")
#
## Plot histogram
#plt.figure(figsize=(12, 6))
#plt.hist(lengths, bins=100, edgecolor='black', alpha=0.7)
#plt.xlabel('Text Length (characters)')
#plt.ylabel('Frequency')
#plt.title('Distribution of Yelp Review Text Lengths')
#plt.grid(True, alpha=0.3)
#
#plt.tight_layout()
#plt.savefig('yelp_text_length_histogram.png', dpi=300)
#plt.show()
#
#print("\nHistogram saved as 'yelp_text_length_histogram.png'")
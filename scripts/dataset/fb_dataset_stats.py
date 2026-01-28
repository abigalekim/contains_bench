file = "/mnt/wiscdb/abigale/string_dataset_csvs/fb_comments.csv"
reviews = []
lengths = []
with open(file, 'r', encoding='utf-8') as fp:
    for line in fp:
        review_data = line.strip()
        lengths.append(len(review_data))

# Print some statistics
print(f"Total reviews: {len(lengths)}")
print(f"Average length: {sum(lengths)/len(lengths):.2f}")
print(f"Min length: {min(lengths)}")
print(f"Max length: {max(lengths)}")
print(f"Median length: {sorted(lengths)[len(lengths)//2]}")
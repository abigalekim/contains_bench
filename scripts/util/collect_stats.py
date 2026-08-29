import csv
import statistics
import sys

csv.field_size_limit(sys.maxsize)

prefix = "/home/akkim7/string_datasets/"

def string_length_stats(filename):
    lengths = []
    with open(prefix + filename, newline='') as f:
        for row in csv.reader(f):
            lengths.append(len(row[0].encode('utf-8')))

    lengths.sort()
    n = len(lengths)
    p95_idx = int(0.95 * n)
    p99_idx = int(0.99 * n)

    print(f"Filename: {filename}")
    print(f"Total strings:     {n}")
    print(f"Longer than 128B:  {sum(1 for l in lengths if l > 128)}")
    print(f"128B or shorter:   {sum(1 for l in lengths if l <= 128)}")
    print(f"Mean length:       {statistics.mean(lengths):.2f}")
    print(f"Median length:     {statistics.median(lengths):.2f}")
    print(f"Std dev:           {statistics.stdev(lengths):.2f}")
    print(f"95th percentile:   {lengths[p95_idx]}")
    print(f"99th percentile:   {lengths[p99_idx]}")

filename = sys.argv[1]
string_length_stats(filename)
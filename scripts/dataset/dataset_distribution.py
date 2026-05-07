import matplotlib.pyplot as plt
import csv
import numpy as np

def process_file(filename):
  f = open(filename, "r")
  f_lines = f.readlines()
  lengths = []
  for i in range(1,len(f_lines)):
    lengths.append(len(f_lines[i]))

  # Print detailed statistics
  print("=" * 60)
  print("DATA STATISTICS")
  print("=" * 60)
  print(f"Total entries: {len(lengths):,}")
  print(f"Min length: {np.min(lengths)}")
  print(f"Max length: {np.max(lengths)}")
  print(f"Mean length: {np.mean(lengths):.2f}")
  print(f"Median length: {np.median(lengths):.2f}")
  print(f"Std deviation: {np.std(lengths):.2f}")
  print("\nPercentiles:")
  for p in [25, 50, 75, 90, 95, 99, 99.9]:
      print(f"  {p}th percentile: {np.percentile(lengths, p):.2f}")
  
  print("=" * 60)
  
  #plt.hist(lengths, bins=15, edgecolor='black')
  #plt.savefig("help.pdf")

process_file("/home/akkim7/string_datasets/twitter_utf8.csv")
import csv
from lorem_text import lorem
import sys
import numpy as np

output_dir = "/home/akkim7/string_datasets"

GIGABYTE = 1073741824
MEGABYTE = 1048576

def generate_text(text_length, starting_word_length):
  wl = starting_word_length
  while True:
    word = lorem.words(wl)
    if len(word) >= text_length:
      return word[:text_length]
    wl += 50

if __name__ == '__main__':
  min_size = int(sys.argv[1])
  max_size = int(sys.argv[2])
  output_filename = "normal_" + str(min_size) + "_" + str(max_size) + ".csv"
  output_file = open(output_dir + "/" + output_filename, "w")
  output_csv = csv.writer(output_file)

  total_bytes = 0
  total_len = 10 * GIGABYTE
  gb_written = 0
  mean = (min_size + max_size) / 2
  std_dev = (max_size - min_size) / 4
  print(f"Starting writing data for normal distribution ({min_size}, {max_size})")
  while total_bytes < total_len:
    string_size = int(np.random.normal(loc=mean, scale=std_dev))
    string_size = max(min_size, min(max_size, string_size))
    string_size = max(1, string_size)
    starting_word_size = (string_size // 5) + 5
    word = generate_text(string_size, starting_word_size)
    output_csv.writerow([word])
    total_bytes += len(word)

    current_gb = total_bytes // GIGABYTE
    if current_gb > gb_written:
      gb_written = current_gb
      print(f"Written {gb_written} GB of data ({total_bytes:,} bytes)")
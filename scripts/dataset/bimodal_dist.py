import csv
from lorem_text import lorem
import sys
import numpy as np
import random

output_dir = "/mnt/wiscdb/abigale/string_dataset_csvs/libcudf_bench"

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
  mean1 = int(sys.argv[1])
  sigma1 = int(sys.argv[2])
  mean2 = int(sys.argv[3])
  sigma2 = int(sys.argv[4])
  output_filename = "bimodal_" + str(mean1) + "_" + str(sigma1) + "_" + str(mean2) + "_" + str(sigma2) + ".csv"
  output_file = open(output_dir + "/" + output_filename, "w")
  output_csv = csv.writer(output_file)

  total_bytes = 0
  total_len = 5 * GIGABYTE
  gb_written = 0

  print(f"Starting writing data for bimodal distribution ({mean1}, {sigma1}), ({mean2}, {sigma2})")
  while total_bytes < total_len:
    small_dist = random.random() < 0.995
    string_size =  int(np.random.normal(loc=mean1, scale=sigma1)) if small_dist else int(np.random.normal(loc=mean2, scale=sigma2))
    string_size = max(1, string_size)
    starting_word_size = (string_size // 5) + 5
    word = generate_text(string_size, starting_word_size)
    output_csv.writerow([word])
    total_bytes += len(word)
#
    current_gb = total_bytes // GIGABYTE
    if current_gb > gb_written:
      gb_written = current_gb
      print(f"Written {gb_written} GB of data ({total_bytes} bytes)")
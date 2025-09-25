import os
import csv
from lorem_text import lorem
import sys

output_mb = 2048
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
  option_str = sys.argv[1]
  string_size = int(sys.argv[2])
  long_string_size = int(sys.argv[3])
  skew = True if option_str == "skew" else False

  if option_str != "uniform" and option_str != "skew":
    sys.exit(-1)
  output_filename = option_str + "_" + str(string_size) + ".csv"
  output_file = open(output_dir + "/" + output_filename, "w")
  output_csv = csv.writer(output_file)

  total_bytes = 0
  total_len = 5 * GIGABYTE
  gb_written = 0
  print("Starting writing data with " + option_str + " dataset with string length " + str(string_size))
  while total_bytes < total_len:
    for i in range(0,300):
      starting_word_size = (string_size // 5) + 5
      word = generate_text(string_size, starting_word_size)
      output_csv.writerow([word])
      total_bytes += len(word)
      if total_bytes >= total_len:
        break

    if skew and total_bytes < total_len:
      long_string_starting_size = (long_string_size // 5) + 5
      long_word = generate_text(long_string_size, long_string_starting_size)
      output_csv.writerow([long_word])
      total_bytes += len(long_word)

    current_gb = total_bytes // GIGABYTE
    if current_gb > gb_written:
      gb_written = current_gb
      print(f"Written {gb_written} GB of data ({total_bytes:,} bytes)")
  
  print("Data has been generated, written to " + output_filename + "\n")
  output_file.close()
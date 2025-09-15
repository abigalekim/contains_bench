
import csv
import os

def split_csv(input_file, output_file1, output_file2=None):
  dirname = "/mnt/wiscdb/abigale/string_dataset_csvs/"
  file = open(dirname + input_file, 'r', newline='', encoding='utf-8')
  reader = csv.reader(file)
  rows = list(reader)

  # Calculate split point
  total_data_rows = len(rows)
  split_point = total_data_rows // 2

  # Split the data
  first_half = rows[:split_point]
  second_half = rows[split_point:]

  # Write first half
  with open(dirname + output_file1, 'w', newline='', encoding='utf-8') as file1:
    writer = csv.writer(file1)
    writer.writerows(first_half)

split_csv("uniform_32.csv", "uniform_32_5gb.csv")
split_csv("uniform_64.csv", "uniform_64_5gb.csv")
split_csv("uniform_128.csv", "uniform_128_5gb.csv")
split_csv("uniform_256.csv", "uniform_256_5gb.csv")
split_csv("uniform_512.csv", "uniform_512_5gb.csv")

split_csv("skew_32.csv", "skew_32_5gb.csv")
split_csv("skew_64.csv", "skew_64_5gb.csv")
split_csv("skew_128.csv", "skew_128_5gb.csv")
split_csv("skew_256.csv", "skew_256_5gb.csv")
split_csv("skew_512.csv", "skew_512_5gb.csv")
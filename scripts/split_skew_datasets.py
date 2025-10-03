import sys
import csv

def process(filename, small, large):
  f = open(filename, "r")
  f_csv = csv.reader(f)
  rows = list(f_csv)
  small_f = open(small, "w")
  small_writer = csv.writer(small_f)
  large_f = open(large, "w")
  large_writer = csv.writer(large_f)
  
  for line in rows:
    if len(line[0]) <= 64:
      small_writer.writerow(line)
    else:
      large_writer.writerow(line)

  f.close()
  small_f.close()
  large_f.close()

if __name__ == '__main__':
  if len(sys.argv) == 3:
    min_size = int(sys.argv[1])
    max_size = int(sys.argv[2])
    normal_filename = "/mnt/wiscdb/abigale/string_dataset_csvs/libcudf_bench/normal_" + str(min_size) + "_" + str(max_size) + ".csv"
    normal_output_small = "/mnt/wiscdb/abigale/string_dataset_csvs/libcudf_bench/normal_small_" + str(min_size) + "_" + str(max_size) + ".csv"
    normal_output_large = "/mnt/wiscdb/abigale/string_dataset_csvs/libcudf_bench/normal_large_" + str(min_size) + "_" + str(max_size) + ".csv"
    print(f"Processing normal distribution ({min_size}, {max_size})")
    process(normal_filename, normal_output_small, normal_output_large)

    uniform_filename = "/mnt/wiscdb/abigale/string_dataset_csvs/libcudf_bench/uniform_dist_" + str(min_size) + "_" + str(max_size) + ".csv"
    uniform_output_small = "/mnt/wiscdb/abigale/string_dataset_csvs/libcudf_bench/uniform_dist_small_" + str(min_size) + "_" + str(max_size) + ".csv"
    uniform_output_large = "/mnt/wiscdb/abigale/string_dataset_csvs/libcudf_bench/uniform_dist_large_" + str(min_size) + "_" + str(max_size) + ".csv"
    print(f"Processing uniform distribution ({min_size}, {max_size})")
    process(uniform_filename, uniform_output_small, uniform_output_large)
  elif len(sys.argv) == 2:
    skew_size = int(sys.argv[1])
    filename = "/mnt/wiscdb/abigale/string_dataset_csvs/libcudf_bench/skew_" + str(skew_size) + ".csv"
    output_small = "/mnt/wiscdb/abigale/string_dataset_csvs/libcudf_bench/skew_small_" + str(skew_size) + ".csv"
    output_large = "/mnt/wiscdb/abigale/string_dataset_csvs/libcudf_bench/skew_large_" + str(skew_size) + ".csv"
    print(f"Processing skew distribution with usual string size {skew_size}")
    process(filename, output_small, output_large)

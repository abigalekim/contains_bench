import os

prefix = "/mnt/wiscdb/abigale/string_dataset_csvs"

small_files = [
  "libcudf_bench/skew_small_16.csv",
  "libcudf_bench/skew_small_32.csv",
  "libcudf_bench/skew_small_64.csv",
  "libcudf_bench/uniform_dist_small_16_128.csv",
  "libcudf_bench/normal_small_16_128.csv",
  "libcudf_bench/bimodal_small_16_5_512_100.csv",
  "libcudf_bench/bimodal_small_32_10_512_100.csv",
  "libcudf_bench/bimodal_small_64_20_512_100.csv",
  "libcudf_bench/bimodal_small_16_5_8192_500.csv",
  "libcudf_bench/bimodal_small_32_10_8192_500.csv",
  "libcudf_bench/bimodal_small_64_20_8192_500.csv",
  "libcudf_bench/bimodal_small_16_5_65536_2000.csv", 
  "libcudf_bench/bimodal_small_32_10_65536_2000.csv",
  "libcudf_bench/bimodal_small_64_20_65536_2000.csv",
  "skew_small_fb_comments.csv",
  "skew_small_fb_posts.csv",
  "skew_small_reddit.csv",
  "skew_small_twitter.csv"
]

large_files = [
  "libcudf_bench/skew_large_16.csv",
  "libcudf_bench/skew_large_32.csv",
  "libcudf_bench/skew_large_64.csv",
  "libcudf_bench/uniform_dist_large_16_128.csv",
  "libcudf_bench/normal_large_16_128.csv",
  "libcudf_bench/bimodal_large_16_5_512_100.csv",
  "libcudf_bench/bimodal_large_32_10_512_100.csv",
  "libcudf_bench/bimodal_large_64_20_512_100.csv",
  "libcudf_bench/bimodal_large_16_5_8192_500.csv",
  "libcudf_bench/bimodal_large_32_10_8192_500.csv",
  "libcudf_bench/bimodal_large_64_20_8192_500.csv",
  "libcudf_bench/bimodal_large_16_5_65536_2000.csv", 
  "libcudf_bench/bimodal_large_32_10_65536_2000.csv",
  "libcudf_bench/bimodal_large_64_20_65536_2000.csv",
  "skew_large_fb_comments.csv",
  "skew_large_fb_posts.csv",
  "skew_large_reddit.csv",
  "skew_large_twitter.csv"
]

#def count_lines_sum_generator(filepath):
#  with open(filepath, 'r') as file:
#    num_lines = sum(1 for line in file)
#  return num_lines
#
#for file in small_files:
#  print(count_lines_sum_generator(os.path.join(prefix, file)))

o = open('output.txt', 'r')
o_lines = o.readlines()

i = 0
while i < len(o_lines):
  # 6 is partition, 7 is thread, 8 is warp
  if o_lines[i].startswith("Filename: "):
    start_idx = i + 8
    total = 0
    for x in range(0,6):
      actual_idx = start_idx + (x * 3)
      num = float(o_lines[actual_idx].split(" ")[3].strip())
      total += num
    print(round(total/6, 2))
    i = i + 25
  else:
    i += 1

o.close()
#o = open('string_output.txt', 'r')
#o_lines = o.readlines()
#
#i = 0
#while i < len(o_lines):
#  if o_lines[i].startswith("Filename: "):
#    num = float(o_lines[i+1].split(" ")[3].strip())
#    print(round(num, 2))
#    i = i + 2
#  else:
#    i += 1
#
#o.close()


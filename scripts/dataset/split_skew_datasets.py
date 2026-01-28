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
  if len(sys.argv) == 1:
    print("Processing Reddit and Twitter datasets")
    dir = "/mnt/wiscdb/abigale/string_dataset_csvs/"
    #process(dir + "reddit_utf8.csv", dir + "skew_small_reddit.csv", dir + "skew_large_reddit.csv")
    #process(dir + "twitter_utf8.csv", dir + "skew_small_twitter.csv", dir + "skew_twitter.csv")
    process(dir + "amazon_arts_and_crafts.csv", dir + "skew_small_amazon_arts_and_crafts.csv", dir + "skew_large_amazon_arts_and_crafts.csv")
    process(dir + "yelp_reviews.csv", dir + "skew_small_yelp_reviews.csv", dir + "skew_large_yelp_reviews.csv")
  elif len(sys.argv) == 2:
    skew_size = int(sys.argv[1])
    filename = "/mnt/wiscdb/abigale/string_dataset_csvs/libcudf_bench/skew_" + str(skew_size) + ".csv"
    output_small = "/mnt/wiscdb/abigale/string_dataset_csvs/libcudf_bench/skew_small_" + str(skew_size) + ".csv"
    output_large = "/mnt/wiscdb/abigale/string_dataset_csvs/libcudf_bench/skew_large_" + str(skew_size) + ".csv"
    print(f"Processing skew distribution with usual string size {skew_size}")
    process(filename, output_small, output_large)
  elif len(sys.argv) == 3:
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
  elif len(sys.argv) == 5:
    mean1 = int(sys.argv[1])
    std1 = int(sys.argv[2])
    mean2 = int(sys.argv[3])
    std2 = int(sys.argv[4])

    bimodal_filename = f'/mnt/wiscdb/abigale/string_dataset_csvs/libcudf_bench/bimodal_{mean1}_{std1}_{mean2}_{std2}.csv'
    bimodal_small = f'/mnt/wiscdb/abigale/string_dataset_csvs/libcudf_bench/bimodal_small_{mean1}_{std1}_{mean2}_{std2}.csv'
    bimodal_large = f'/mnt/wiscdb/abigale/string_dataset_csvs/libcudf_bench/bimodal_large_{mean1}_{std1}_{mean2}_{std2}.csv'
    print(f'Processing bimodal distribution ({mean1}, {std1}), ({mean2},{std2})')
    process(bimodal_filename, bimodal_small, bimodal_large)

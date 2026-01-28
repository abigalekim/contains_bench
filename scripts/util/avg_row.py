import csv
import sys 
csv.field_size_limit(sys.maxsize)

def average_row_length(filename):
  with open(filename, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    
    sum = 0
    total_rows = 0
    for row in reader:
      sum += len(row[0])
      total_rows += 1
    
    print(round(sum/total_rows, 2))

prefix = "/mnt/wiscdb/abigale/string_dataset_csvs/"
#average_row_length(prefix + "libcudf_bench/skew_16.csv")
#average_row_length(prefix + "libcudf_bench/skew_32.csv")
#average_row_length(prefix + "libcudf_bench/skew_64.csv")
#average_row_length(prefix + "libcudf_bench/uniform_dist_16_128.csv")
#average_row_length(prefix + "libcudf_bench/normal_16_128.csv")
#average_row_length(prefix + "libcudf_bench/bimodal_16_5_512_100.csv")
#average_row_length(prefix + "libcudf_bench/bimodal_32_10_512_100.csv")
#average_row_length(prefix + "libcudf_bench/bimodal_64_20_512_100.csv")
#average_row_length(prefix + "libcudf_bench/bimodal_16_5_8192_500.csv")
#average_row_length(prefix + "libcudf_bench/bimodal_32_10_8192_500.csv")
#average_row_length(prefix + "libcudf_bench/bimodal_64_20_8192_500.csv")
#average_row_length(prefix + "libcudf_bench/bimodal_16_5_65536_2000.csv")
#average_row_length(prefix + "libcudf_bench/bimodal_32_10_65536_2000.csv")
#average_row_length(prefix + "libcudf_bench/bimodal_64_20_65536_2000.csv")
#average_row_length(prefix + "fb_comments.csv")
#average_row_length(prefix + "fb_posts.csv")
#average_row_length(prefix + "reddit.csv")
#average_row_length(prefix + "twitter.csv")
#average_row_length(prefix + "amazon_arts_and_crafts.csv")
#average_row_length(prefix + "yelp_reviews.csv")
average_row_length(prefix + "github_commits.csv")
average_row_length(prefix + "common_crawl_urls.csv")
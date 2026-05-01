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

def number_of_lines(filename):
    with open(filename, 'r', encoding='utf-8', errors='replace') as f:
        # Filter NUL bytes which cause csv.Error
        reader = csv.reader(x.replace('\x00', '') for x in f)
        total_rows = sum(1 for row in reader)
        print(total_rows)
    return total_rows

prefix = "/home/akkim7/string_datasets/"
#number_of_lines(prefix + "skew_16.csv")
#number_of_lines(prefix + "skew_32.csv")
#number_of_lines(prefix + "skew_64.csv")
#number_of_lines(prefix + "uniform_dist_16_128.csv")
#number_of_lines(prefix + "normal_16_128.csv")
#number_of_lines(prefix + "bimodal_16_5_512_100.csv")
#number_of_lines(prefix + "bimodal_32_10_512_100.csv")
#number_of_lines(prefix + "bimodal_64_20_512_100.csv")
#number_of_lines(prefix + "bimodal_16_5_8192_500.csv")
#number_of_lines(prefix + "bimodal_32_10_8192_500.csv")
#number_of_lines(prefix + "bimodal_64_20_8192_500.csv")
#number_of_lines(prefix + "bimodal_16_5_65536_2000.csv")
#number_of_lines(prefix + "bimodal_32_10_65536_2000.csv")
#number_of_lines(prefix + "bimodal_64_20_65536_2000.csv")
#number_of_lines(prefix + "fb_comments.csv")
#number_of_lines(prefix + "fb_posts.csv")
#number_of_lines(prefix + "reddit_utf8.csv")
#number_of_lines(prefix + "twitter_utf8.csv")
number_of_lines(prefix + "amazon_arts_and_crafts.csv")
number_of_lines(prefix + "yelp_reviews.csv")
number_of_lines(prefix + "github_commits.csv")
number_of_lines(prefix + "common_crawl_urls.csv")
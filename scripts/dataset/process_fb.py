import csv

dir = "/home/akkim7/string_datasets/"
GIGABYTE = 1073741824

def process_csv(input_filename, index, output_filename):
  ifname = dir + input_filename
  ifobj = open(ifname, "r")
  ifcsvobj = csv.reader(ifobj)

  ofname = dir + output_filename
  ofobj = open(ofname, "w")
  ofcsvobj = csv.writer(ofobj)

  inputrows = list(ifcsvobj)
  print(len(inputrows))

  total_bytes = 0
  total_len = 3 * GIGABYTE
  gb_written = 0
  row_idx = 0

  while total_bytes < total_len and row_idx < len(inputrows):
    message = inputrows[row_idx][index]
    row_idx += 1
    if row_idx == len(inputrows):
      row_idx = 0

    total_bytes += len(message)
    ofcsvobj.writerow([message.replace("\n", "")])

    current_gb = total_bytes // GIGABYTE
    if current_gb > gb_written:
      gb_written = current_gb
      print(f"Written {gb_written} GB of data ({total_bytes:,} bytes)")

  ifobj.close()
  ofobj.close()

  print("Data has been generated")
  

comment_input_file = "fb_news_comments_1000K_hashed.csv"
post_input_file = "fb_news_posts_20K.csv"
process_csv(comment_input_file, 3, "fb_comments.csv")
process_csv(post_input_file, 3, "fb_posts.csv")
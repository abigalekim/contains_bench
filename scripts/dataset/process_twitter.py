import csv

input_path = "/home/akkim7/.cache/kagglehub/datasets/kazanova/sentiment140/versions/2/training.1600000.processed.noemoticon.csv"
output_path = "/home/akkim7/string_datasets/twitter_utf8.csv"
GIGABYTE = 1073741824

# Read with latin-1 (won't throw errors), write as UTF-8
with open(input_path, "r", encoding="latin-1") as f_in:
  f_csv = csv.reader(f_in)
  f_csv_rows = list(f_csv)
  
  with open(output_path, "w", encoding="utf-8", newline='') as f_out:
    writer = csv.writer(f_out)
      
    total_bytes = 0
    total_len = 10 * GIGABYTE
    gb_written = 0
    row_idx = 0

    while total_bytes < total_len:
      message = f_csv_rows[row_idx][5]
      row_idx += 1
      if row_idx == len(f_csv_rows):
        row_idx = 0

      total_bytes += len(message)
      writer.writerow([message.replace("\n","")])

      current_gb = total_bytes // GIGABYTE
      if current_gb > gb_written:
        gb_written = current_gb
        print(f"Written {gb_written} GB of data ({total_bytes:,} bytes)")

print("Done! File converted to UTF-8")
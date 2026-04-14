import sys, os, time
 
def extract_comments(tbl_path, output_path, target_bytes):
    print(f"Reading {tbl_path} ...")
    comments = []
    with open(tbl_path) as f:
        for line in f:
            parts = line.rstrip("|\n").split("|")
            comments.append(parts[15])
    print(f"  Loaded {len(comments):,} comments")
 
    header = "value\n"
    written, row_count, idx = 0, 0, 0
    n = len(comments)
    start = time.time()
 
    with open(output_path, "w", buffering=1<<20) as out:
        out.write(header)
        written += len(header.encode())
        while written < target_bytes:
            comment = comments[idx % n]
            row = f'"{comment.replace(chr(34), chr(34)*2)}"\n'
            out.write(row)
            written += len(row.encode())
            row_count += 1; idx += 1
            if row_count % 200_000 == 0:
                e = time.time() - start
                print(f"  {written/target_bytes*100:5.1f}%  {written/1e6:.1f} MB  {written/1e6/e:.1f} MB/s", end="\r")
 
    print(f"\nDone! {row_count:,} rows, {os.path.getsize(output_path)/1e9:.3f} GB")
 
tbl = sys.argv[1]
out = sys.argv[2]
gb  = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
extract_comments(tbl, out, int(gb * 1e9))
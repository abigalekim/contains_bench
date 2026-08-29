#!/usr/bin/env python3
"""
Parse exp5.txt (or any similarly formatted het timing output) and print
per-dataset averages of hot runs for Partition, Thread, Warp, and total
query execution time.

Output is tab-separated, ready to paste into a CSV.

Usage:
    python parse_exp5_times.py --input ../../results/exp5.txt
"""

import re
import argparse


def parse_exp5(text):
    """
    Split the flat file into per-dataset blocks and extract:
      - partition_avg  : mean of hot Partition times
      - thread_avg     : mean of hot Thread times
      - warp_avg       : mean of hot Warp times
      - query_avg      : Contains query average (already computed by the bench)

    "Hot runs" = all runs after the first (cold) run.
    The cold run is identified as the first set of Partition/Thread/Warp values
    printed for each dataset block (before "Running cold run..." resets nothing —
    the bench just prints one cold set then N hot sets sequentially).
    """
    blocks = re.split(r"Filename:\s*(\S+)", text)
    # blocks = ['', fname1, body1, fname2, body2, ...]

    results = []
    it = iter(blocks[1:])
    for fname, body in zip(it, it):
        partition_vals = [float(v) for v in re.findall(r"Partition time:\s*([\d.]+)", body)]
        thread_vals    = [float(v) for v in re.findall(r"Thread time:\s*([\d.]+)",    body)]
        warp_vals      = [float(v) for v in re.findall(r"Warp time:\s*([\d.]+)",      body)]
        query_m        = re.search(r"Contains query average:\s*([\d.]+)", body)

        # Drop index 0 (cold run) from each
        hot_partition = partition_vals[1:] if len(partition_vals) > 1 else []
        hot_thread    = thread_vals[1:]    if len(thread_vals)    > 1 else []
        hot_warp      = warp_vals[1:]      if len(warp_vals)      > 1 else []

        def avg(lst):
            return sum(lst) / len(lst) if lst else None

        results.append({
            "filename":      fname,
            "partition_avg": avg(hot_partition),
            "thread_avg":    avg(hot_thread),
            "warp_avg":      avg(hot_warp),
            "query_avg":     float(query_m.group(1)) if query_m else None,
        })

    return results


def fmt(val):
    return f"{val:.6f}" if val is not None else "N/A"


def main():
    parser = argparse.ArgumentParser(description="Parse exp5 het timing output.")
    parser.add_argument("--input", "-i", default="exp5.txt",
                        help="Path to the exp5 timing file (default: exp5.txt)")
    args = parser.parse_args()

    with open(args.input, "r") as f:
        text = f.read()

    results = parse_exp5(text)

    # Header
    print("\t".join(["filename", "partition_avg_ms", "thread_avg_ms",
                     "warp_avg_ms", "query_avg_ms"]))

    for r in results:
        print("\t".join([
            r["filename"],
            fmt(r["partition_avg"]),
            fmt(r["thread_avg"]),
            fmt(r["warp_avg"]),
            fmt(r["query_avg"]),
        ]))


if __name__ == "__main__":
    main()
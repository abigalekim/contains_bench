#!/usr/bin/env python3
"""
Parse NCU profiles for cudf and het implementations and emit a CSV with
one row per workload and columns for each metric per implementation/kernel.

Het has TWO kernels:
  - transform_kernel         (partition step)
  - contains_warp_parallel_fn_heterogeneous  (main step)

Cudf has ONE kernel:
  - contains_warp_parallel_fn

Metrics extracted per kernel:
  - Compute (SM) Throughput %
  - Memory Throughput %
  - smsp__average_thread_inst_executed_per_inst_executed.ratio
  - smsp__warps_issue_stalled_long_scoreboard.sum

Output CSV columns:
  workload,
  het_transform_compute_sm_pct, het_transform_memory_pct,
  het_transform_thread_inst_ratio, het_transform_stalled_long_scoreboard,
  het_main_compute_sm_pct, het_main_memory_pct,
  het_main_thread_inst_ratio, het_main_stalled_long_scoreboard,
  cudf_compute_sm_pct, cudf_memory_pct,
  cudf_thread_inst_ratio, cudf_stalled_long_scoreboard

Usage:
    python parse_ncu_comparison.py --profiles-dir /path/to/profiles/
"""

import re
import os
import csv
import argparse
import sys

BENCHMARKS = [
    ("skew_16",                   "skew_16"),
    ("skew_32",                   "skew_32"),
    ("skew_64",                   "skew_64"),
    ("uniform_dist_16_128",       "uniform"),
    ("normal_16_128",             "normal"),
    ("bimodal_16_5_512_100",      "bimodal_16_5_512_100"),
    ("bimodal_32_10_512_100",     "bimodal_32_10_512_100"),
    ("bimodal_64_20_512_100",     "bimodal_64_20_512_100"),
    ("bimodal_16_5_8192_500",     "bimodal_16_5_8192_500"),
    ("bimodal_32_10_8192_500",    "bimodal_32_10_8192_500"),
    ("bimodal_64_20_8192_500",    "bimodal_64_20_8192_500"),
    ("bimodal_16_5_65536_2000",   "bimodal_16_5_65536_2000"),
    ("bimodal_32_10_65536_2000",  "bimodal_32_10_65536_2000"),
    ("bimodal_64_20_65536_2000",  "bimodal_64_20_65536_2000"),
    ("fb_comments",               "fb_comments"),
    ("fb_posts",                  "fb_posts"),
    ("reddit_utf8",               "reddit"),
    ("twitter_utf8",              "twitter"),
    ("amazon_arts_and_crafts",    "amazon"),
    ("yelp_reviews",              "yelp"),
    ("github_commits",            "github"),
    ("common_crawl_urls",         "urls"),
]

# ── Metric patterns ───────────────────────────────────────────────────────────
METRICS = {
    "compute_sm_pct":          re.compile(r'Compute \(SM\) Throughput\s+%\s+([\d.]+)'),
    "memory_pct":              re.compile(r'Memory Throughput\s+%\s+([\d.]+)'),
    "thread_inst_ratio":       re.compile(r'smsp__average_thread_inst_executed_per_inst_executed\.ratio\s+([\d.]+)'),
    "stalled_long_scoreboard": re.compile(r'smsp__warps_issue_stalled_long_scoreboard\.sum\s+warp\s+([\d.]+)'),
    "l1_requests":             re.compile(r'l1tex__t_requests_pipe_lsu_mem_global_op_ld\.sum\s+([\d.]+)'),
}

BLOCK_START = re.compile(r'^\s{2}\S.*\(\d+,\s*\d+,\s*\d+\)x\(\d+')


def classify_kernel(raw_line):
    """
    Return one of: 'transform', 'het_main', 'cudf_main', or None.

    cudf kernels appear in two forms depending on the benchmark:
      1. unnamed>::contains_warp_parallel_fn(...)        -> contains_warp_parallel_fn, no _heterogeneous
      2. void transform_kernel<...contains_fn<contains(  -> transform_kernel wrapping contains_fn
         (this is the cudf single-kernel path for shorter strings)

    het kernels:
      - transform_kernel<...contains_heterogeneous...>   -> het partition step
      - contains_warp_parallel_fn_heterogeneous(...)     -> het main kernel
    """
    # Must check het_main first: its name contains contains_warp_parallel_fn as substring
    if re.search(r'contains_warp_parallel_fn_heterogeneous', raw_line):
        return "het_main"
    # Het partition kernel: transform_kernel that references contains_heterogeneous
    if re.search(r'transform_kernel', raw_line) and re.search(r'contains_heterogeneous', raw_line):
        return "transform"
    # cudf form 1: plain contains_warp_parallel_fn (no _heterogeneous suffix)
    if re.search(r'contains_warp_parallel_fn', raw_line):
        return "cudf_main"
    # cudf form 2: transform_kernel wrapping contains_fn (no contains_heterogeneous)
    if re.search(r'transform_kernel', raw_line) and re.search(r'contains_fn', raw_line):
        return "cudf_main"
    return None


def parse_file(filepath):
    """
    Parse an NCU text file and return a dict keyed by kernel label.
    Each value is a dict of metric_name -> float (or None if not found).
    Only kernels we care about (transform, het_main, cudf_main) are kept.
    """
    results = {}          # label -> {metric: value}
    current_label = None
    current_metrics = {}

    with open(filepath, 'r', errors='replace') as f:
        lines = f.readlines()

    for line in lines:
        if BLOCK_START.match(line):
            # Save previous kernel if relevant
            if current_label is not None:
                results[current_label] = current_metrics

            label = classify_kernel(line)
            current_label = label
            current_metrics = {k: None for k in METRICS}
            continue

        if current_label is not None:
            for metric_key, pat in METRICS.items():
                m = pat.search(line)
                if m and current_metrics[metric_key] is None:
                    current_metrics[metric_key] = float(m.group(1))

    # Save last kernel
    if current_label is not None:
        results[current_label] = current_metrics

    return results


def find_file(profiles_dir, impl, bench_suffix):
    path = os.path.join(profiles_dir, impl, f"{impl}_{bench_suffix}.txt")
    return path if os.path.exists(path) else None


def metrics_row(kernel_data, label_prefix):
    """
    Given a dict of {metric_key: value_or_None} and a column prefix,
    return an ordered list of (column_name, value_string) pairs.
    """
    row = []
    for metric_key in METRICS:
        col = f"{label_prefix}_{metric_key}"
        val = kernel_data.get(metric_key) if kernel_data else None
        row.append((col, "" if val is None else str(val)))
    return row


def main():
    parser = argparse.ArgumentParser(
        description="Compare NCU metrics for het and cudf implementations."
    )
    parser.add_argument(
        "--profiles-dir", "-d",
        default="../../profiles",
        help="Path to the profiles/ directory (default: ../../profiles)"
    )
    parser.add_argument(
        "--output", "-o",
        default="ncu_comparison.csv",
        help="Output CSV file path (default: ncu_comparison.csv)"
    )
    args = parser.parse_args()

    profiles_dir = args.profiles_dir

    # Build header
    metric_keys = list(METRICS.keys())
    header = ["workload"]
    for prefix in ["het_transform", "het_main", "cudf"]:
        for mk in metric_keys:
            header.append(f"{prefix}_{mk}")

    rows = []

    for dataset_name, bench_suffix in BENCHMARKS:
        row = {"workload": dataset_name}

        # ── HET ──────────────────────────────────────────────────────────────
        het_file = find_file(profiles_dir, "het", bench_suffix)
        if het_file:
            parsed = parse_file(het_file)
            transform_data = parsed.get("transform")
            het_main_data  = parsed.get("het_main")
        else:
            print(f"[WARN] Missing het file for {dataset_name}", file=sys.stderr)
            transform_data = None
            het_main_data  = None

        for col, val in metrics_row(transform_data, "het_transform"):
            row[col] = val
        for col, val in metrics_row(het_main_data, "het_main"):
            row[col] = val

        # ── CUDF ─────────────────────────────────────────────────────────────
        cudf_file = find_file(profiles_dir, "cudf", bench_suffix)
        if cudf_file:
            parsed = parse_file(cudf_file)
            cudf_data = parsed.get("cudf_main")
        else:
            print(f"[WARN] Missing cudf file for {dataset_name}", file=sys.stderr)
            cudf_data = None

        for col, val in metrics_row(cudf_data, "cudf"):
            row[col] = val

        rows.append(row)

    # ── Write CSV ─────────────────────────────────────────────────────────────
    with open(args.output, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Written {len(rows)} rows to {args.output}")


if __name__ == "__main__":
    main()
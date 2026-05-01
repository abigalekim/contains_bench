#!/usr/bin/env python3
"""
Parse NCU Speed of Light profiles and print Compute (SM) Throughput + Memory Throughput
in benchmark order, one row per benchmark per implementation.

Output format (tab-separated, ready to paste into CSV):
  For single-kernel methods: benchmark_name  compute%  memory%
  For two-kernel methods:    benchmark_name  k1_compute%  k1_memory%  k2_compute%  k2_memory%

Usage:
    python parse_ncu_profiles.py --profiles-dir /path/to/profiles/
"""

import re
import os
import argparse

# ── Benchmark order and their file stem suffixes ──────────────────────────────
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

IMPLEMENTATIONS = ["het", "cudf", "thread", "warp", "badhet"]

# Methods that profile TWO kernels (transform_kernel first, then the main kernel)
TWO_KERNEL_METHODS = {"het", "badhet"}


def parse_file(filepath):
    """
    Parse an NCU profile text file and return a list of dicts, one per kernel profiled.
    Each dict: {'kernel_name': str, 'compute_sm': float, 'memory': float}
    Kernels are returned in the order they appear in the file.
    """
    kernels = []
    current_kernel = None

    compute_pat = re.compile(r'Compute \(SM\) Throughput\s+%\s+([\d.]+)')
    memory_pat  = re.compile(r'Memory Throughput\s+%\s+([\d.]+)')
    # A kernel header line looks like:  "  KernelName(...) (grid)x(block), ..."
    kernel_header_pat = re.compile(r'^\s{2}(\S.*?)\s*\(\d+')

    with open(filepath, 'r', errors='replace') as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i]

        # Detect start of a new kernel block
        # NCU output indents kernel names with exactly 2 spaces before the name,
        # followed by a launch config like (N, 1, 1)x(256, 1, 1)
        if re.match(r'^\s{2}\S', line) and re.search(r'\(\d+,\s*\d+,\s*\d+\)x\(\d+', line):
            if current_kernel is not None:
                kernels.append(current_kernel)
            # Extract a short readable name from the full mangled name
            raw = line.strip()
            # Grab everything up to the first '(' of the launch config
            name_part = re.split(r'\s*\(\d+,\s*1,\s*1\)', raw)[0].strip()
            current_kernel = {'kernel_name': name_part, 'compute_sm': None, 'memory': None}

        if current_kernel is not None:
            m = compute_pat.search(line)
            if m:
                current_kernel['compute_sm'] = float(m.group(1))
            m = memory_pat.search(line)
            if m:
                current_kernel['memory'] = float(m.group(1))

        i += 1

    if current_kernel is not None:
        kernels.append(current_kernel)

    return kernels


def find_profile_file(profiles_dir, impl, bench_suffix):
    """
    Locate the profile file for a given implementation and benchmark suffix.
    Naming convention: profiles/<impl>/<impl>_<bench_suffix>.txt
    """
    base = os.path.join(profiles_dir, impl, f"{impl}_{bench_suffix}")
    for ext in [".txt"]:
        path = base + ext
        if os.path.exists(path):
            return path
    return None


def main():
    parser = argparse.ArgumentParser(description="Parse NCU SOL profiles into tabular output.")
    parser.add_argument(
        "--profiles-dir", "-d",
        default="../../profiles",
        help="Path to the profiles/ directory (default: ./profiles)"
    )
    args = parser.parse_args()

    profiles_dir = args.profiles_dir

    print("# Columns for single-kernel methods (cudf, thread, warp):")
    print("#   benchmark | compute_sm% | memory%")
    print("# Columns for two-kernel methods (het, badhet):")
    print("#   benchmark | k1_compute_sm% | k1_memory% | k2_compute_sm% | k2_memory%")
    print()

    for impl in IMPLEMENTATIONS:
        print(f"=== {impl.upper()} ===")
        two_kernels = impl in TWO_KERNEL_METHODS

        for dataset_name, bench_suffix in BENCHMARKS:
            filepath = find_profile_file(profiles_dir, impl, bench_suffix)

            if filepath is None:
                if two_kernels:
                    print(f"{dataset_name}\tMISSING\tMISSING\tMISSING\tMISSING")
                else:
                    print(f"{dataset_name}\tMISSING\tMISSING")
                continue

            kernels = parse_file(filepath)

            if two_kernels:
                if len(kernels) >= 2:
                    k1, k2 = kernels[0], kernels[1]
                    c1 = f"{k1['compute_sm']}" if k1['compute_sm'] is not None else "N/A"
                    m1 = f"{k1['memory']}"     if k1['memory']     is not None else "N/A"
                    c2 = f"{k2['compute_sm']}" if k2['compute_sm'] is not None else "N/A"
                    m2 = f"{k2['memory']}"     if k2['memory']     is not None else "N/A"
                    print(f"{dataset_name}\t{c1}\t{m1}\t{c2}\t{m2}")
                elif len(kernels) == 1:
                    k1 = kernels[0]
                    c1 = f"{k1['compute_sm']}" if k1['compute_sm'] is not None else "N/A"
                    m1 = f"{k1['memory']}"     if k1['memory']     is not None else "N/A"
                    print(f"{dataset_name}\t{c1}\t{m1}\tN/A\tN/A")
                else:
                    print(f"{dataset_name}\tPARSE_ERROR\tPARSE_ERROR\tPARSE_ERROR\tPARSE_ERROR")
            else:
                if len(kernels) >= 1:
                    k1 = kernels[0]
                    c1 = f"{k1['compute_sm']}" if k1['compute_sm'] is not None else "N/A"
                    m1 = f"{k1['memory']}"     if k1['memory']     is not None else "N/A"
                    print(f"{dataset_name}\t{c1}\t{m1}")
                else:
                    print(f"{dataset_name}\tPARSE_ERROR\tPARSE_ERROR")

        print()


if __name__ == "__main__":
    main()
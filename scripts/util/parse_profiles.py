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


def short_kernel_name(mangled):
    """
    Extract a short, human-readable kernel name from a mangled NCU kernel name.
    Examples:
      'void cub::transform_kernel<...contains_heterogeneous...'  -> 'transform_kernel'
      'contains_warp_parallel_fn_heterogeneous(...'              -> 'contains_warp_parallel_fn_heterogeneous'
      'contains_warp_parallel_fn(...'                            -> 'contains_warp_parallel_fn'
      'unnamed>::contains_fn<contains_thread...'                 -> 'contains_fn'
    """
    patterns = [
        r'contains_warp_parallel_fn_heterogeneous(?:_bad)?',
        r'contains_warp_parallel_fn',
        r'transform_kernel',
        r'contains_fn',
    ]
    for pat in patterns:
        m = re.search(pat, mangled)
        if m:
            return m.group(0)
    # Fallback: first token before '<' or '('
    return re.split(r'[<(]', mangled)[0].strip()


def parse_file(filepath):
    """
    Parse an NCU profile text file and return a list of dicts, one per relevant kernel.
    Each dict: {'kernel_name': str, 'compute_sm': float, 'memory': float}
    """
    kernels = []
    current_kernel = None
    current_relevant = True
 
    compute_pat = re.compile(r'Compute \(SM\) Throughput\s+%\s+([\d.]+)')
    memory_pat  = re.compile(r'Memory Throughput\s+%\s+([\d.]+)')
 
    with open(filepath, 'r', errors='replace') as f:
        lines = f.readlines()
 
    for line in lines:
        if re.match(r'^\s{2}\S', line) and re.search(r'\(\d+,\s*\d+,\s*\d+\)x\(\d+', line):
            if current_kernel is not None and current_relevant:
                kernels.append(current_kernel)
 
            raw = line.strip()
            name_part = re.split(r'\s*\(\d+,\s*1,\s*1\)', raw)[0].strip()
            current_kernel = {
                'kernel_name': short_kernel_name(name_part),
                'compute_sm': None,
                'memory': None,
            }
 
            if 'transform_kernel' in name_part and 'contains_heterogeneous' not in name_part and 'contains_fn' not in name_part:
                current_relevant = False
            else:
                current_relevant = True
 
        if current_kernel is not None and current_relevant:
            m = compute_pat.search(line)
            if m:
                current_kernel['compute_sm'] = float(m.group(1))
            m = memory_pat.search(line)
            if m:
                current_kernel['memory'] = float(m.group(1))
 
    if current_kernel is not None and current_relevant:
        kernels.append(current_kernel)
 
    return kernels
 
 
def find_profile_file(profiles_dir, impl, bench_suffix):
    base = os.path.join(profiles_dir, impl, f"{impl}_{bench_suffix}.txt")
    if os.path.exists(base):
        return base
    return None


def discover_kernel_names(profiles_dir):
    """
    Scan the first available file for each method class to discover actual kernel names.
    Returns (single_kernel_name, [two_k1_name, two_k2_name]).
    """
    single_name = None
    two_names = [None, None]

    for impl in IMPLEMENTATIONS:
        for _, bench_suffix in BENCHMARKS:
            fp = find_profile_file(profiles_dir, impl, bench_suffix)
            if fp is None:
                continue
            kernels = parse_file(fp)
            if impl in TWO_KERNEL_METHODS:
                if len(kernels) >= 2 and two_names[0] is None:
                    two_names = [kernels[0]['kernel_name'], kernels[1]['kernel_name']]
            else:
                if len(kernels) >= 1 and single_name is None:
                    single_name = kernels[0]['kernel_name']
            if single_name and two_names[0]:
                break
        if single_name and two_names[0]:
            break

    return single_name or "kernel", two_names[0] or "k1", two_names[1] or "k2"


def main():
    parser = argparse.ArgumentParser(description="Parse NCU SOL profiles into tabular output.")
    parser.add_argument(
        "--profiles-dir", "-d",
        default="../../profiles",
        help="Path to the profiles/ directory (default: ../../profiles)"
    )
    args = parser.parse_args()
 
    profiles_dir = args.profiles_dir

    single_name, k1_name, k2_name = discover_kernel_names(profiles_dir)

    print("# Columns for single-kernel methods (cudf, thread, warp):")
    print(f"#   benchmark | {single_name}_compute_sm% | {single_name}_memory%")
    print("# Columns for two-kernel methods (het, badhet):")
    print(f"#   benchmark | {k1_name}_compute_sm% | {k1_name}_memory% | {k2_name}_compute_sm% | {k2_name}_memory%")
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
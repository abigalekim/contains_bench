import re
import os
import argparse
import sys

BENCHMARKS = [
    ("skew_16"),
    ("skew_32"),
    ("skew_64"),
    ("bimodal_16_5_512_100"),
    ("bimodal_32_10_512_100"),
    ("bimodal_64_20_512_100"),
    ("bimodal_16_5_8192_500"),
    ("bimodal_32_10_8192_500"),
    ("bimodal_64_20_8192_500"),
    ("bimodal_16_5_65536_2000"),
    ("bimodal_32_10_65536_2000"),
    ("bimodal_64_20_65536_2000"),
]

METRICS = {
    "l1_requests":         re.compile(r'l1tex__t_requests_pipe_lsu_mem_global_op_ld\.sum\s+([\d.]+)'),
    "l1_hit_rate":         re.compile(r'l1tex__t_sector_hit_rate\.pct\s+([\d.]+)'),
    "avg_thread_per_inst": re.compile(r'smsp__average_thread_inst_executed_per_inst_executed\.ratio\s+([\d.]+)'),
    "long_scoreboard_sum": re.compile(r'smsp__warps_issue_stalled_long_scoreboard\.sum\s+warp\s+([\d.]+)'),
}

# Maps --impl value to (profiles subdir, kernel label to extract)
IMPL_CONFIG = ["het", "cudf", "thread", "warp"]

BLOCK_START = re.compile(r'^\s{2}\S.*\(\d+,\s*\d+,\s*\d+\)x\(\d+')


def classify_kernel(raw_line):
    if re.search(r'contains_warp_parallel_fn_heterogeneous', raw_line):
        return "het_warp"
    if re.search(r'transform_kernel', raw_line) and re.search(r'contains_heterogeneous', raw_line):
        return "transform"
    if re.search(r'contains_warp_parallel_fn', raw_line):
        return "cudf_warp"
    if re.search(r'transform_kernel', raw_line) and re.search(r'contains_fn', raw_line):
        return "transform"
    return None


def parse_file(filepath, kernel, metric_pat):
    results = {}
    current_label = None
    current_val = None

    with open(filepath, 'r', errors='replace') as f:
        lines = f.readlines()

    for line in lines:
        if BLOCK_START.match(line):
            if current_label is not None:
                results[current_label] = current_val
            k_name = classify_kernel(line)
            current_label = k_name if k_name == kernel else None
            current_val = None
            continue

        if current_label is not None and current_val is None:
            m = metric_pat.search(line)
            if m:
                current_val = float(m.group(1))

    if current_label is not None:
        results[current_label] = current_val

    return results


def find_file(profiles_dir, subdir, bench_suffix):
    path = os.path.join(profiles_dir, subdir, f"{subdir}_{bench_suffix}.txt")
    return path if os.path.exists(path) else None


def main():
    parser = argparse.ArgumentParser(
        description="Print a single NCU metric for a fixed set of workloads."
    )
    parser.add_argument(
        "metric",
        choices=list(METRICS.keys()),
        help="Metric to extract: " + ", ".join(METRICS.keys())
    )
    parser.add_argument(
        "--profiles-dir", "-d",
        default="../../profiles",
        help="Path to the profiles/ directory (default: ../../profiles)"
    )
    parser.add_argument(
        "--impl",
        choices=list(IMPL_CONFIG),
        default="het",
        help="Implementation to read from: het (default), cudf, thread, warp"
    )
    parser.add_argument(
        "--kernel",
        choices=["het_warp", "transform", "cudf_warp"],
        default=None,
        help="Override which kernel to extract the metric from (overrides --impl default)."
    )
    args = parser.parse_args()

    metric_pat = METRICS[args.metric]
    kernel = args.kernel

    for dataset_name in BENCHMARKS:
        filepath = find_file(args.profiles_dir, args.impl, dataset_name)
        if not filepath:
            print("", file=sys.stdout)
            print(f"[WARN] Missing {args.impl} file for {dataset_name}", file=sys.stderr)
            continue

        parsed = parse_file(filepath, kernel, metric_pat)
        val = parsed.get(kernel)
        print("" if val is None else val)


if __name__ == "__main__":
    main()
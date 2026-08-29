#!/usr/bin/env python3
"""
Parse NCU Speed of Light profiles from profiles/exp5/pct_<value>.txt
and print Compute (SM) Throughput + Memory Throughput for each kernel.

Usage:
    python parse_exp5.py --profiles-dir ../../profiles
"""

import re
import os
import argparse

PCT_VALUES = ["0.1", "0.5", "1.0", "5.0", "10.0", "25.0", "50.0",
              "75.0", "90.0", "95.0", "99.0", "99.5", "99.9"]

# Reused from the main script
def short_kernel_name(mangled):
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
    return re.split(r'[<(]', mangled)[0].strip()

def parse_file(filepath):
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
            # Skip stray replace_character_parallel transform_kernels
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

def main():
    parser = argparse.ArgumentParser(description="Parse NCU SOL profiles for exp5 pct sweep.")
    parser.add_argument("--profiles-dir", "-d", default="../../profiles",
                        help="Path to the profiles/ directory (default: ../../profiles)")
    args = parser.parse_args()

    exp5_dir = os.path.join(args.profiles_dir, "exp5")

    # Discover how many kernels we're dealing with from the first available file
    kernel_names = []
    for pct in PCT_VALUES:
        fp = os.path.join(exp5_dir, f"cudf_pct_{pct}.txt")
        if os.path.exists(fp):
            kernels = parse_file(fp)
            kernel_names = [k['kernel_name'] for k in kernels]
            break

    # Print header
    header_parts = ["pct"]
    for name in kernel_names:
        header_parts += [f"{name}_compute_sm%", f"{name}_memory%"]
    print("\t".join(header_parts))

    # Print one row per pct file
    for pct in PCT_VALUES:
        fp = os.path.join(exp5_dir, f"pct_{pct}.txt")
        if not os.path.exists(fp):
            missing = "\t".join(["MISSING"] * (len(kernel_names) * 2))
            print(f"{pct}\t{missing}")
            continue

        kernels = parse_file(fp)
        row = [pct]
        for k in kernels:
            row.append(str(k['compute_sm']) if k['compute_sm'] is not None else "N/A")
            row.append(str(k['memory'])     if k['memory']     is not None else "N/A")
        print("\t".join(row))

if __name__ == "__main__":
    main()
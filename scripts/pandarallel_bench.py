#!/usr/bin/env python3
import pandas as pd
import sys
import time
from pandarallel import pandarallel

def main():
    if len(sys.argv) < 2:
        print("Error: did not pass enough arguments", file=sys.stderr)
        return 1

    filename = sys.argv[1]
    print(f"Filename: {filename}")
    csv_filename = f"/home/akkim7/string_datasets/{filename}"
    request = "Harum Hic Ex At"

    # Initialize pandarallel (verbose=1 shows worker info, progress_bar=False keeps output clean)
    pandarallel.initialize(progress_bar=False, verbose=1)

    # Read CSV - treat each line as a single value
    print("Reading CSV...")
    with open(csv_filename, 'r') as f:
        lines = [line.rstrip('\n') for line in f]
    df = pd.DataFrame({'value': lines})
    print(f"Loaded {len(df)} rows")

    # Cold run
    print("Running cold run...")
    result = df['value'].parallel_apply(lambda s: request in s)

    # Hot run
    print("Running hot run...")
    start_time = time.perf_counter()
    result = df['value'].parallel_apply(lambda s: request in s)
    end_time = time.perf_counter()
    hot_time = (end_time - start_time) * 1000
    print(f"Hot run time: {hot_time:.5f} ms")

    # Benchmark runs
    times = []
    for i in range(5):
        start_time = time.perf_counter()
        result = df['value'].parallel_apply(lambda s: request in s)
        end_time = time.perf_counter()
        times.append((end_time - start_time) * 1000)

    avg_time = sum(times) / len(times)
    print(f"Contains query average: {avg_time:.5f} ms")
    return 0

if __name__ == "__main__":
    sys.exit(main())
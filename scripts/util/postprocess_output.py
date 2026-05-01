import re

path = "/Users/abigale/code/uwmadison/contains_bench/results/04-27-2026/fb_output.txt"

with open(path) as f:
    text = f.read()

# ── helpers ──────────────────────────────────────────────────────────────────

def get_query_averages(section_text):
    """Return {filename: avg_ms} for every dataset that has a query average."""
    blocks = re.split(r"Filename:\s*(\S+)", section_text)
    result = {}
    # blocks = ['', fname1, body1, fname2, body2, ...]
    it = iter(blocks[1:])
    for fname, body in zip(it, it):
        m = re.search(r"Contains query average:\s*([\d.]+)", body)
        if m:
            result[fname] = float(m.group(1))
    return result


def get_component_avgs(section_text, label):
    """
    For het / bad-het sections: for each dataset block, collect all
    `<label> time: X ms` values, drop the first one (cold run), and
    return the mean of the remaining hot runs.
    Returns {filename: avg_ms} for datasets that have this label.
    """
    blocks = re.split(r"Filename:\s*(\S+)", section_text)
    result = {}
    it = iter(blocks[1:])
    for fname, body in zip(it, it):
        vals = [float(v) for v in re.findall(rf"{label} time:\s*([\d.]+)\s*ms", body)]
        if len(vals) > 1:            # need at least 1 cold + 1 hot run
            hot = vals[1:]
            result[fname] = sum(hot) / len(hot)
        # if 0 or 1 values, skip (empty / cold-only dataset)
    return result


def print_section(title, data):
    print(f"\n=== {title} ===")
    for fname, avg in data.items():
        print(f"  {fname:45s}  {avg:.6f} ms")


# ── split into named sections ─────────────────────────────────────────────────

section_pattern = re.compile(
    r"^(het bench|bad het bench|cudf bench|thread bench|warp bench)\s*$",
    re.MULTILINE,
)
parts = section_pattern.split(text)
# parts = ['<preamble>', 'het bench', '<het body>', 'bad het bench', '<bad het body>', ...]
sections = {}
it = iter(parts[1:])
for name, body in zip(it, it):
    sections[name] = body

het     = sections.get("het bench", "")
bad_het = sections.get("bad het bench", "")
cudf    = sections.get("cudf bench", "")
thread  = sections.get("thread bench", "")
warp    = sections.get("warp bench", "")

# ── het component times ───────────────────────────────────────────────────────

print_section("Het  – Avg Partition Times (hot runs only)", get_component_avgs(het, "Partition"))
print_section("Het  – Avg Thread Exec Times (hot runs only)", get_component_avgs(het, "Thread"))
print_section("Het  – Avg Warp Exec Times (hot runs only)", get_component_avgs(het, "Warp"))

# ── bad-het component times ───────────────────────────────────────────────────

print_section("Bad-Het – Avg Thread Exec Times (hot runs only)", get_component_avgs(bad_het, "Thread"))
print_section("Bad-Het – Avg Warp Exec Times (hot runs only)", get_component_avgs(bad_het, "Warp"))

# ── query averages for all methods ───────────────────────────────────────────

print_section("Query Avg – het",     get_query_averages(het))
print_section("Query Avg – bad het", get_query_averages(bad_het))
print_section("Query Avg – cudf",    get_query_averages(cudf))
print_section("Query Avg – thread",  get_query_averages(thread))
print_section("Query Avg – warp",    get_query_averages(warp))
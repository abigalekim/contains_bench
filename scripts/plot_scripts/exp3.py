import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import re

# ===== CONFIG =====
CSV_PATH = "../csv/exp3.csv"
FONT_PATH = "/Users/abigale/code/fonts/LinLibertineOTF_5.3.0_2012_07_02/LinBiolinum_R.otf"
# ==================

custom_font = fm.FontEntry(fname=FONT_PATH, name="Linux Biolinum")
fm.fontManager.ttflist.insert(0, custom_font)

plt.style.use('seaborn-v0_8-paper')
plt.rcParams['font.family'] = "serif"
plt.rcParams.update({
    "axes.labelsize": 14,
    "legend.fontsize": 14,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "axes.titlesize": 14,
    "grid.alpha": 0.3,
    "text.usetex": False
})

color_set = ['#f77189', '#dc8932', '#ae9d31', '#77ab31', '#33b07a', '#36ada4',
             '#38a9c5', '#6e9bf4', '#cc7af4', '#f565cc']


def format_label(name):
    name_str = str(name).lower().strip()
    if 'skew' in name_str:
        val = name_str.split()[-1]
        alpha = {'16': '1.6', '32': '3.2', '64': '6.4'}.get(val, val)
        return rf"S($\alpha={alpha}$)"
    if 'uniform' in name_str:
        return "U(16,128)"
    if 'normal' in name_str:
        return "N(16,128)"
    if 'bimodal' in name_str:
        nums = re.findall(r'\((\d+),', name_str)
        if len(nums) >= 2:
            return rf"B($\mu_1={nums[0]},\mu_2={nums[1]}$)"
        return name.title()

    mapping = {
        'facebook comments': 'FB Comments',
        'facebook posts': 'FB Posts',
        'reddit comments': 'Reddit',
        'twitter posts': 'Twitter',
        'amazon reviews': 'Amazon',
        'yelp reviews': 'Yelp',
        'github': 'Commit Msgs',
        'common urls': 'URLs'
    }
    return mapping.get(name_str, name.title())


# Load data
df = pd.read_csv(CSV_PATH)
df = df.loc[:, ~df.columns.str.match(r'^Unnamed')]
df['formal_label'] = df['dataset'].apply(format_label)


# ===== GRAPH 1: Stacked Breakdown + libcudf/thread/warp (custom scale broken axis) =====
x = np.arange(len(df))
bar_width = 0.21

p = df['breakdown_partition'].values
t = df['breakdown_thread'].values
w = df['breakdown_warp'].values

# Break point: values <= 50 get lower half, values > 50 get upper half
BREAK = 50
MAX_VAL = 385

def forward(ticks):
    ticks = np.array(ticks, dtype=float)
    ticks = np.where(ticks <= BREAK, 0.5 * (ticks / BREAK), ticks)
    ticks = np.where(ticks > BREAK,  0.5 + 0.5 * ((ticks - BREAK) / (MAX_VAL - BREAK)), ticks)
    return ticks

def inverse(ticks):
    ticks = np.array(ticks, dtype=float)
    ticks = np.where(ticks <= 0.5, ticks * BREAK / 0.5, ticks)
    ticks = np.where(ticks > 0.5,  BREAK + (ticks - 0.5) * (MAX_VAL - BREAK) / 0.5, ticks)
    return ticks

fig, ax = plt.subplots(figsize=(16, 6))
ax.set_yscale('function', functions=(forward, inverse))

# Draw bars
ax.bar(x - 1.5 * bar_width, p, bar_width, label='Het: Partitioning',
       color=color_set[6], edgecolor='black', linewidth=0.5)
ax.bar(x - 1.5 * bar_width, t, bar_width, bottom=p,
       label='Het: Thread Execution',
       color=color_set[7], edgecolor='black', linewidth=0.5)
ax.bar(x - 1.5 * bar_width, w, bar_width, bottom=p + t,
       label='Het: Warp Execution',
       color=color_set[8], edgecolor='black', linewidth=0.5)
ax.bar(x - 0.5 * bar_width, df['libcudf'].values, bar_width, label='libcudf 25.10',
       color=color_set[1], edgecolor='black', linewidth=0.5)
ax.bar(x + 0.5 * bar_width, df['thread'].values,  bar_width, label='Thread per String',
       color=color_set[3], edgecolor='black', linewidth=0.5)
ax.bar(x + 1.5 * bar_width, df['warp'].values,    bar_width, label='Warp per String',
       color=color_set[0], edgecolor='black', linewidth=0.5)

# Y-axis ticks: dense below break, sparse above
y_ticks = [0, 10, 20, 30, 40, 50, 100, 150, 200, 250, 300, 350]
ax.set_yticks(y_ticks)
ax.set_ylim(0, MAX_VAL)
ax.yaxis.grid(True, linestyle='--', alpha=0.3)
ax.set_axisbelow(True)

# Draw // break markers on y-axis at break point
d = 0.25
break_y = forward(np.array([BREAK]))[0]
kwargs = dict(marker=[(-1, -d), (1, d)], markersize=10, linestyle='none',
              color='k', mec='k', mew=1, clip_on=False)
ax.plot([0], [break_y], transform=ax.transAxes, **kwargs)

ax.set_ylabel('Execution Time (ms)')
ax.set_xticks(x)
ax.set_xticklabels(df['formal_label'], rotation=40, ha='right')
ax.legend(frameon=True, loc='upper center', bbox_to_anchor=(0.5, -0.45),
          ncol=6, handlelength=1.5, columnspacing=1.0)

plt.tight_layout()
plt.subplots_adjust(bottom=0.32)
plt.savefig('exp3_breakdown_all.pdf', dpi=300, bbox_inches='tight')
plt.close()
print("Generated: exp3_breakdown_all.pdf")


# ===== GRAPH 2: Scatter — Input Size vs Partitioning Time (All Workloads) =====
fig, ax = plt.subplots(figsize=(10, 5))

ax.scatter(df['input_size'], df['breakdown_partition'],
           color=color_set[0], edgecolors='black', linewidths=0.5,
           s=70, zorder=3)

ax.set_xlabel('Input Size (bytes)')
ax.set_ylabel('Partitioning Time (ms)')
ax.grid(linestyle='--')
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim(1e7, 1e9)
ax.set_xticks([1e7, 2e7, 5e7, 1e8, 2e8, 5e8, 1e9])
ax.set_yticks([2,4,6,8,10])
ax.set_yticklabels([2,4,6,8,10])
ax.set_xticklabels(['$10^7$', r'$2\times10^7$', r'$5\times10^7$', '$10^8$', r'$2\times10^8$', r'$5\times10^8$', '$10^9$'])
ax.set_ylim(0, 14)
ax.set_yticks([2, 4, 6, 8, 10, 12, 14])

plt.tight_layout()
plt.savefig('exp3_partition_vs_input_size.pdf', dpi=300, bbox_inches='tight')
plt.close()
print("Generated: exp3_partition_vs_input_size.pdf")

print("\n✓ Done!")
print("  - exp3_breakdown_all.pdf")
print("  - exp3_partition_vs_input_size.pdf")
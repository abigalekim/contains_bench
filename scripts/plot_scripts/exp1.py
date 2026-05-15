import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import re

# ===== CONFIG =====
CSV_PATH = "../csv/exp1.csv"
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
    if 'bimodal' in name_str:
        nums = re.findall(r'\((\d+),', name_str)
        if len(nums) >= 2:
            return rf"B($\mu_1={nums[0]},\mu_2={nums[1]}$)"
        return name.title()
    return name.title()


# Load data and compute speedups normalized to libcudf
df = pd.read_csv(CSV_PATH)
df['formal_label'] = df['dataset'].apply(format_label)
df['speedup_het']       = df['libcudf'] / df['het']
df['speedup_thread']    = df['libcudf'] / df['thread']
df['speedup_warp']      = df['libcudf'] / df['warp']
df['speedup_dataframe'] = df['libcudf'] / df['dataframe']
df['speedup_pandas']    = df['libcudf'] / df['pandas']

BREAK = 1.0
MAX_VAL = df[['speedup_het', 'speedup_thread', 'speedup_warp', 'speedup_dataframe']].values.max() * 1.05

def forward(ticks):
    ticks = np.array(ticks, dtype=float)
    ticks = np.where(ticks <= BREAK, (1/4) * (ticks / BREAK), ticks)
    ticks = np.where(ticks > BREAK,  (1/4) + (3/4) * ((ticks - BREAK) / (MAX_VAL - BREAK)), ticks)
    return ticks

def inverse(ticks):
    ticks = np.array(ticks, dtype=float)
    ticks = np.where(ticks <= 1/4, ticks * BREAK / (1/4), ticks)
    ticks = np.where(ticks > 1/4,  BREAK + (ticks - 1/4) * (MAX_VAL - BREAK) / (3/4), ticks)
    return ticks


x = np.arange(len(df))
width = 0.12

fig, ax = plt.subplots(figsize=(13, 5))
ax.set_yscale('function', functions=(forward, inverse))

ax.bar(x - 2.5 * width, df['speedup_het'].values,       width, label='Heterogeneous',
       color=color_set[0], edgecolor='black', linewidth=0.5)
ax.bar(x - 1.5 * width, df['speedup_thread'].values,    width, label='Thread per String',
       color=color_set[3], edgecolor='black', linewidth=0.5)
ax.bar(x - 0.5 * width, df['speedup_warp'].values,      width, label='Warp per String',
       color=color_set[7], edgecolor='black', linewidth=0.5)
ax.bar(x + 0.5 * width, np.ones(len(df)),               width, label='libcudf 25.10',
       color=color_set[1], edgecolor='black', linewidth=0.5)
ax.bar(x + 1.5 * width, df['speedup_dataframe'].values, width, label='C++ DataFrame Lib',
       color=color_set[2], edgecolor='black', linewidth=0.5)
ax.bar(x + 2.5 * width, df['speedup_pandas'].values,    width, label='Pandas',
       color=color_set[4], edgecolor='black', linewidth=0.5)

# Y-axis ticks: dense below break, sparse above
ax.set_yticks([0.5, 1, 5, 10, 15])
ax.set_ylim(0, MAX_VAL)
ax.yaxis.grid(True, linestyle='--', alpha=0.3)
ax.set_axisbelow(True)
ax.axhline(y=1.0, color='gray', linestyle='--', linewidth=1.2, zorder=0)

# Draw // break markers
d = 0.25
break_y = forward(np.array([BREAK]))[0]
kwargs = dict(marker=[(-1, -d), (1, d)], markersize=10, linestyle='none',
              color='k', mec='k', mew=1, clip_on=False)
ax.plot([0], [break_y - 0.01], transform=ax.transAxes, **kwargs)
ax.plot([0], [break_y + 0.01], transform=ax.transAxes, **kwargs)

ax.set_ylabel('Speedup over libcudf (×)')
ax.set_xticks(x)
ax.set_xticklabels(df['formal_label'], rotation=40, ha='right')
ax.legend(frameon=True, loc='upper right')

plt.tight_layout()
plt.savefig('exp1_speedup_vs_libcudf.pdf', dpi=300, bbox_inches='tight')


plt.close()
print("Generated: exp1_speedup_vs_libcudf.pdf")
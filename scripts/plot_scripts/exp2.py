import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import re

# ===== CONFIG =====
CSV_PATH = "../csv/exp2.csv"
FONT_PATH = "/Users/abigale/code/fonts/LinLibertineOTF_5.3.0_2012_07_02/LinBiolinum_R.otf"
# ==================

custom_font = fm.FontEntry(fname=FONT_PATH, name="Linux Biolinum")
fm.fontManager.ttflist.insert(0, custom_font)

plt.style.use('seaborn-v0_8-paper')
plt.rcParams['font.family'] = "serif"
plt.rcParams.update({
    "axes.labelsize": 14,
    "legend.fontsize": 13,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "axes.titlesize": 14,
    "grid.alpha": 0.3,
    "text.usetex": False
})

color_set = ['#f77189', '#dc8932', '#ae9d31', '#77ab31', '#33b07a', '#36ada4',
             '#38a9c5', '#6e9bf4', '#cc7af4', '#f565cc']


def format_label(name):
    name_str = str(name).lower().strip().replace('_', ' ')
    if 'skew' in name_str:
        val = name_str.split()[-1]
        alpha = {'16': '1.6', '32': '3.2', '64': '6.4'}.get(val, val)
        return rf"S($\alpha={alpha}$)"
    if 'uniform' in name_str:
        return "U(16,128)"
    if 'normal' in name_str:
        return "N(16,128)"
    if 'bimodal' in name_str:
        nums = re.findall(r'\((\d+),', name_str) or re.findall(r'(\d+)', name_str)
        if len(nums) >= 3:
            return rf"B($\mu_1={nums[0]},\mu_2={nums[2]}$)"
        elif len(nums) >= 2:
            return rf"B($\mu_1={nums[0]},\mu_2={nums[1]}$)"
        return name.title()

    mapping = {
        'fb comments': 'FB Comments',
        'fb posts': 'FB Posts',
        'reddit utf8': 'Reddit',
        'twitter utf8': 'Twitter',
        'amazon arts and crafts': 'Amazon',
        'yelp reviews': 'Yelp',
        'github commits': 'Commit Msgs',
        'common crawl urls': 'URLs',
        'facebook comments': 'FB Comments',
        'facebook posts': 'FB Posts',
        'reddit comments': 'Reddit',
        'twitter posts': 'Twitter',
        'amazon reviews': 'Amazon',
        'github': 'Commit Msgs',
        'common urls': 'URLs'
    }
    return mapping.get(name_str, name.title())


# Load and label data
df = pd.read_csv(CSV_PATH)
name_col = 'workload' if 'workload' in df.columns else 'dataset'
df['formal_label'] = df[name_col].apply(format_label)

rw_keywords = ['fb comments', 'fb posts', 'reddit', 'twitter', 'amazon',
               'yelp', 'github', 'common crawl', 'facebook', 'common urls']
df['is_rw'] = df[name_col].str.lower().str.replace('_', ' ').apply(
    lambda n: any(kw in n for kw in rw_keywords)
)
df_rw  = df[df['is_rw']].copy()
df_syn = df[~df['is_rw']].copy()
df_all = pd.concat([df_syn, df_rw], ignore_index=True)


# ===== GRAPH 1: Thread Instruction Ratio (All Workloads) =====
# Columns: het_transform (thread kernel), het_main (warp kernel),
#          cudf kernel, thread-per-string impl, warp-per-string impl
fig, ax = plt.subplots(figsize=(12, 6))

x = np.arange(len(df_all))
width = 0.15

ax.bar(x - 2 * width, df_all['het_thread_avg_thread_per_inst'].values, width,
       label='Het Transform Kernel (thread)', color=color_set[7],
       edgecolor='black', linewidth=0.5)
ax.bar(x - 1 * width, df_all['het_warp_avg_thread_per_inst'].values, width,
       label='Het Main Kernel (warp)', color=color_set[8],
       edgecolor='black', linewidth=0.5)
ax.bar(x,              df_all['cudf_avg_thread_per_inst'].values, width,
       label='cuDF Kernel', color=color_set[1],
       edgecolor='black', linewidth=0.5)
ax.bar(x + 1 * width,  df_all['thread_avg_thread_per_inst'].values, width,
       label='Thread per String', color=color_set[3],
       edgecolor='black', linewidth=0.5)
ax.bar(x + 2 * width,  df_all['warp_avg_thread_per_inst'].values, width,
       label='Warp per String', color=color_set[0],
       edgecolor='black', linewidth=0.5)

ax.axhline(y=32, color='gray', linestyle='--', linewidth=1.2, label='Ideal (32)')

ax.set_ylabel('Average Active Threads per Instruction', labelpad=12)
ax.set_ylim(0, 36)
ax.set_xticks(x)
ax.set_xticklabels(df_all['formal_label'], rotation=40, ha='right')
ax.grid(axis='y', linestyle='--')
ax.legend(frameon=True, loc='upper center', bbox_to_anchor=(0.5, -0.42),
          ncol=3, handlelength=1.5, columnspacing=1.0)

plt.tight_layout()
plt.subplots_adjust(bottom=0.32)
plt.savefig('exp2_thread_inst_ratio_all.pdf', dpi=300, bbox_inches='tight')
plt.close()
print("Generated: exp2_thread_inst_ratio_all.pdf")


# ===== GRAPH 2: L1 Cache Requests (All Workloads) =====
fig, ax = plt.subplots(figsize=(12, 5))

ax.bar(x - 2 * width, df_all['het_thread_l1_requests'].values, width,
       label='Het Transform Kernel (thread)', color=color_set[7],
       edgecolor='black', linewidth=0.5)
ax.bar(x - 1 * width, df_all['het_warp_l1_requests'].values, width,
       label='Het Main Kernel (warp)', color=color_set[8],
       edgecolor='black', linewidth=0.5)
ax.bar(x,              df_all['cudf_l1_requests'].values, width,
       label='cuDF Kernel', color=color_set[1],
       edgecolor='black', linewidth=0.5)
ax.bar(x + 1 * width,  df_all['thread_l1_requests'].values, width,
       label='Thread per String', color=color_set[3],
       edgecolor='black', linewidth=0.5)
ax.bar(x + 2 * width,  df_all['warp_l1_requests'].values, width,
       label='Warp per String', color=color_set[0],
       edgecolor='black', linewidth=0.5)

ax.set_ylabel('L1 Cache Requests')
ax.set_xticks(x)
ax.set_xticklabels(df_all['formal_label'], rotation=40, ha='right')
ax.grid(axis='y', linestyle='--')
ax.yaxis.set_major_formatter(
    matplotlib.ticker.FuncFormatter(
        lambda v, _: f'{v/1e9:.1f}B' if v >= 1e9 else f'{v/1e6:.0f}M'
    )
)
ax.legend(frameon=True, loc='upper center', bbox_to_anchor=(0.5, -0.42),
          ncol=3, handlelength=1.5, columnspacing=1.0)

plt.tight_layout()
plt.subplots_adjust(bottom=0.15)
plt.savefig('exp2_l1_requests_all.pdf', dpi=300, bbox_inches='tight')
plt.close()
print("Generated: exp2_l1_requests_all.pdf")

print("\n✓ Done!")
print("  - exp2_thread_inst_ratio_all.pdf")
print("  - exp2_l1_requests_all.pdf")
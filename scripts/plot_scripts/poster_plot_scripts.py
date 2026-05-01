import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import re

# ===== CONFIG =====
CSV_PATH = "~/Downloads/string_benchmarking_04-22-2026.csv"  # <-- fill in your CSV path here
# ==================

plt.style.use('seaborn-v0_8-paper')
plt.rcParams['font.family'] = "serif"
plt.rcParams.update({
    "axes.labelsize": 13,
    "legend.fontsize": 12,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "axes.titlesize": 14,
    "grid.alpha": 0.3,
    "text.usetex": False
})

color_set = ['#f77189', '#dc8932', '#ae9d31', '#77ab31', '#33b07a', '#36ada4', '#38a9c5', '#6e9bf4', '#cc7af4', '#f565cc']


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
        'facebook comments': 'FB_Comments',
        'facebook posts': 'FB_Posts',
        'reddit comments': 'Reddit',
        'twitter posts': 'Twitter',
        'amazon reviews': 'Amazon',
        'yelp reviews': 'Yelp',
        'github': 'Commit_Msgs',
        'common urls': 'URLs'
    }
    return mapping.get(name_str, name.title())


# Load data
df = pd.read_csv(CSV_PATH)
df['formal_label'] = df['dataset'].apply(format_label)

rw_datasets = ['facebook comments', 'facebook posts', 'reddit comments', 'twitter posts',
               'amazon reviews', 'yelp reviews', 'github', 'common URLs']
df_rw = df[df['dataset'].str.lower().str.strip().isin([d.lower() for d in rw_datasets])].copy()
df_syn = df[~df.index.isin(df_rw.index)].copy()


# ===== 1. COMBINED PERFORMANCE: SYNTHETIC (left) + REAL WORLD (right) =====
fig, (ax_syn, ax_rw) = plt.subplots(1, 2, figsize=(18, 5), sharey=False)

def plot_4way(ax, data, rotation=0, ha="center"):
    x = np.arange(len(data))
    width = 0.2
    bars = [
        ('Heterogeneous',     data['het'].values,    color_set[0]),
        ('libcudf 25.10',     data['libcudf'].values, color_set[1]),
        ('Warp per String',   data['warp'].values,    color_set[2]),
        ('Thread per String', data['thread'].values,  color_set[3]),
    ]
    for i, (label, values, color) in enumerate(bars):
        offset = (i - 1.5) * width
        ax.bar(x + offset, values, width, label=label, color=color, edgecolor='black', linewidth=0.5)
    ax.set_ylabel('Execution Time (ms)')
    ax.set_xticks(x)
    ax.set_xticklabels(data["formal_label"], rotation=rotation, ha=ha)
    ax.grid(axis='y', linestyle='--')

plot_4way(ax_syn, df_syn, rotation=40, ha="right")
ax_syn.set_title('Synthetic Workloads', fontweight='bold', pad=10)

plot_4way(ax_rw, df_rw)
ax_rw.set_title('Real World Workloads', fontweight='bold', pad=10)

handles, labels = ax_syn.get_legend_handles_labels()
perf_labels = ['Heterogeneous', 'libcudf 25.10', 'Warp per String', 'Thread per String']
fig.legend(handles, perf_labels, frameon=True, loc='lower center',
           bbox_to_anchor=(0.5, -0.08), fontsize=12, ncol=4,
           handleheight=1.2, handlelength=2.0, columnspacing=2.0)

plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.savefig('performance_combined.pdf', dpi=300, bbox_inches='tight')
plt.close()
print("Generated: performance_combined.pdf")


# ===== 2. COMBINED BREAKDOWN: SYNTHETIC (left) + REAL WORLD (right) =====
fig, (ax_syn, ax_rw) = plt.subplots(1, 2, figsize=(18, 5), sharey=False)

def plot_breakdown(ax, data, rotation=0, ha="center"):
    x = np.arange(len(data))
    width = 0.6
    ax.bar(x, data['breakdown_partition'].values, width, label='Partitioning',
           color=color_set[6], edgecolor='black', linewidth=0.5)
    ax.bar(x, data['breakdown_thread'].values, width, bottom=data['breakdown_partition'].values,
           label='Thread per String Execution', color=color_set[7], edgecolor='black', linewidth=0.5)
    ax.bar(x, data['breakdown_warp'].values, width,
           bottom=(data['breakdown_partition'] + data['breakdown_thread']).values,
           label='Warp per String Execution', color=color_set[8], edgecolor='black', linewidth=0.5)
    ax.set_ylabel('Execution Time (ms)')
    ax.set_xticks(x)
    ax.set_xticklabels(data["formal_label"], rotation=rotation, ha=ha)
    ax.grid(axis='y', linestyle='--')

plot_breakdown(ax_syn, df_syn, rotation=40, ha="right")
ax_syn.set_title('Synthetic Workloads', fontweight='bold', pad=10)

plot_breakdown(ax_rw, df_rw)
ax_rw.set_title('Real World Workloads', fontweight='bold', pad=10)

handles, labels = ax_syn.get_legend_handles_labels()
breakdown_labels = ['Partitioning', 'Thread per String Execution', 'Warp per String Execution']
fig.legend(handles, breakdown_labels, frameon=True, loc='lower center',
           bbox_to_anchor=(0.5, -0.08), fontsize=12, ncol=3,
           handleheight=1.2, handlelength=2.0, columnspacing=2.0)

plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.savefig('breakdown_combined.pdf', dpi=300, bbox_inches='tight')
plt.close()
print("Generated: breakdown_combined.pdf")


# ===== 3. PARTITIONING TIME VS INPUT SIZE SCATTER =====
fig, ax = plt.subplots(figsize=(10, 5))

ax.scatter(df_syn['input_size'], df_syn['breakdown_partition'],
           color=color_set[0], edgecolors='black', linewidths=0.5, s=70, zorder=3, label='Synthetic')
ax.scatter(df_rw['input_size'], df_rw['breakdown_partition'],
           color=color_set[9], edgecolors='black', linewidths=0.5, s=70, zorder=3, label='Real World')

ax.set_xlabel('Input Size (bytes)')
ax.set_ylabel('Partitioning Time (ms)')
ax.legend(frameon=True, loc='upper left', fontsize=9)
ax.grid(linestyle='--')
plt.tight_layout()
plt.savefig('partition_vs_size.pdf', dpi=300, bbox_inches='tight')
plt.close()
print("Generated: partition_vs_size.pdf")

print("\n✓ All plots generated successfully!")
print("Generated files:")
print("  - performance_combined.pdf")
print("  - breakdown_combined.pdf")
print("  - partition_vs_size.pdf")
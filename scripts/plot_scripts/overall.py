
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import re
 
# ===== CONFIG =====
CSV_PATH = "../csv/overall.csv"
FONT_PATH = "/Users/abigale/Downloads/LinBiolinum_R.otf"  # update if needed
# ==================
 
custom_font = fm.FontEntry(fname=FONT_PATH, name="Linux Biolinum")
fm.fontManager.ttflist.insert(0, custom_font)
 
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
 
 
# Load and split data
df = pd.read_csv(CSV_PATH)
df['formal_label'] = df['dataset'].apply(format_label)
 
rw_datasets = ['facebook comments', 'facebook posts', 'reddit comments', 'twitter posts',
               'amazon reviews', 'yelp reviews', 'github', 'common urls']
df_rw = df[df['dataset'].str.lower().str.strip().isin(rw_datasets)].copy()
df_syn = df[~df.index.isin(df_rw.index)].copy()
 
 
def plot_4way(data, title, filename, rotation=40, ha="right"):
    fig, ax = plt.subplots(figsize=(10, 5))
 
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
        ax.bar(x + offset, values, width, label=label, color=color,
               edgecolor='black', linewidth=0.5)
 
    ax.set_title(title, fontweight='bold', pad=12)
    ax.set_ylabel('Execution Time (ms)')
    ax.set_xticks(x)
    ax.set_xticklabels(data['formal_label'], rotation=rotation, ha=ha)
    ax.grid(axis='y', linestyle='--')
    ax.legend(frameon=True, bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=11)
 
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {filename}")
 
 
plot_4way(df_syn, 'Synthetic Workload Performance', 'overall_synthetic.pdf', rotation=40, ha='right')
plot_4way(df_rw,  'Real World Workload Performance', 'overall_real_world.pdf', rotation=30, ha='right')
 
print("\n✓ Done!")
print("  - overall_synthetic.pdf")
print("  - overall_real_world.pdf")

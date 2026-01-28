import pandas as pd
import matplotlib
matplotlib.use('Agg') # Required for headless servers
import matplotlib.pyplot as plt
import numpy as np

# Updated global style settings for ACM/Libertine look
plt.style.use('seaborn-v0_8-paper')
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Linux Biolinum O", "Biolinum", "Arial", "sans-serif"],
    "axes.labelsize": 11,
    "legend.fontsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 10,
    "axes.titlesize": 13,
    "grid.alpha": 0.3,
    "text.usetex": False
})

def format_label(name):
    """Formalizes workload names for paper-quality legends."""
    name = str(name).lower()
    if 'skew' in name:
        val = name.split()[-1]
        alpha = {'16': '1.6', '32': '3.2', '64': '6.4'}.get(val, val)
        return rf"Skewed ($\alpha={alpha}$)"
    if 'uniform' in name:
        return "Uniform (16, 128)"
    if 'normal' in name:
        return "Normal (16, 128)"
    if 'bimodal' in name:
        parts = name.replace('bimodal', '').replace('(', '').replace(')', '').split()
        if len(parts) >= 2:
            mu1 = parts[0].split(',')[0]
            mu2 = parts[1].split(',')[0]
            return rf"Bimodal ($\mu_1={mu1}, \mu_2={mu2}$)"
        return name.capitalize()
    
    mapping = {
        'facebook comments (5gb)': 'FB Comments',
        'facebook posts (5gb)': 'FB Posts',
        'reddit comments (5gb)': 'Reddit Comm.',
        'twitter posts (5gb)': 'Twitter Posts',
        'amazon reviews': 'Amazon Reviews',
        'yelp reviews': 'Yelp Reviews',
        'github': 'GitHub',
        'common urls': 'Common URLs'
    }
    return mapping.get(name, name.title())

# 1. Load data
df = pd.read_csv('string_benchmarking.csv')
df['formal_label'] = df['dataset'].apply(format_label)

# Split data
fb_idx = df[df['dataset'].str.contains('facebook comments', case=False)].index[0]
df_syn = df.iloc[:fb_idx]
df_rw = df.iloc[fb_idx:]

colors = ['#4C72B0', '#DD8452']
width = 0.35

# --- IMAGE 1: SYNTHETIC ---
fig1, ax1 = plt.subplots(figsize=(8, 5))
x1 = np.arange(len(df_syn))
ax1.bar(x1 - width/2, df_syn['het_times'], width, label='Heterogeneous Times', color=colors[0], edgecolor='black', linewidth=0.6)
ax1.bar(x1 + width/2, df_syn['libcudf'], width, label='libcudf 25.10', color=colors[1], edgecolor='black', linewidth=0.6)
ax1.set_title('Performance Comparison: Synthetic Workloads', fontweight='bold', pad=15)
ax1.set_ylabel('Execution Time (ms)')
ax1.set_xticks(x1)
ax1.set_xticklabels(df_syn['formal_label'], rotation=40, ha='right')
ax1.grid(axis='y', linestyle='--')
ax1.legend(frameon=True, loc='upper left')
plt.tight_layout()
plt.savefig('../figures/synthetic_benchmarks.png', dpi=300, bbox_inches='tight')

# --- IMAGE 2: REAL-WORLD ---
fig2, ax2 = plt.subplots(figsize=(7, 5))
x2 = np.arange(len(df_rw))
ax2.bar(x2 - width/2, df_rw['het_times'], width, label='Heterogeneous Times', color=colors[0], edgecolor='black', linewidth=0.6)
ax2.bar(x2 + width/2, df_rw['libcudf'], width, label='libcudf 25.10', color=colors[1], edgecolor='black', linewidth=0.6)
ax2.set_title('Performance Comparison: Real-World Workloads', fontweight='bold', pad=15)
ax2.set_ylabel('Execution Time (ms)')
ax2.set_xticks(x2)
ax2.set_xticklabels(df_rw['formal_label'], rotation=40, ha='right')
ax2.grid(axis='y', linestyle='--')
ax2.legend(frameon=True, loc='upper left')
plt.tight_layout()
plt.savefig('../figures/realworld_benchmarks.png', dpi=300, bbox_inches='tight')

print("Successfully generated images with Linux Biolinum font.")
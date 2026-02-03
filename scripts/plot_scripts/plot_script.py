import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Required for headless servers
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

# Updated global style settings for ACM/Libertine look
plt.style.use('seaborn-v0_8-paper')
filename = "/Users/abigale/Downloads/LinBiolinum_R.otf"
custom_font = fm.FontEntry(fname=filename, name="Linux Biolinum")
fm.fontManager.ttflist.insert(0, custom_font)
plt.rcParams['font.family'] = "serif"
plt.rcParams.update({
    "axes.labelsize": 11,
    "legend.fontsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 10,
    "axes.titlesize": 13,
    "grid.alpha": 0.3,
    "text.usetex": False
})

# Color scheme
color_set = ['#f77189', '#dc8932', '#ae9d31', '#77ab31', '#33b07a', '#36ada4', '#38a9c5', '#6e9bf4', '#cc7af4', '#f565cc']


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
        'facebook comments (5gb)': 'Facebook Comments',
        'facebook posts (5gb)': 'Facebook Posts',
        'reddit comments (5gb)': 'Reddit Comments',
        'twitter posts (5gb)': 'Twitter Posts',
        'amazon reviews': 'Amazon Reviews',
        'yelp reviews': 'Yelp Reviews',
        'github': 'GitHub URLs',
        'common urls': 'Common URLs'
    }
    return mapping.get(name, name.title())


# Load data
df = pd.read_csv('csv/string_benchmarking.csv')
df['formal_label'] = df['dataset'].apply(format_label)

# Split data into synthetic and Real World
fb_idx = df[df['dataset'].str.contains('facebook comments', case=False)].index[0]
df_syn = df.iloc[:fb_idx].copy()
df_rw = df.iloc[fb_idx:].copy()


# ===== 1. 6-WAY COMPARISON BAR GRAPHS =====
def create_6way_comparison(data, title, filename):
    """Create 6-way comparison bar graph."""
    fig, ax = plt.subplots(figsize=(12, 5))
    
    x = np.arange(len(data))
    width = 0.14
    
    bars = [
        ('Heterogeneous', data['het_times'], color_set[0]),
        ('libcudf 25.10', data['libcudf'], color_set[1]),
        ('Warp per String', data['contains_warp'], color_set[2]),
        ('Thread per String', data['contains_thread'], color_set[3]),
        ('Pandas', data['pandas'], color_set[4]),
        ('DataFrame', data['dataframe'], color_set[5])
    ]
    
    for i, (label, values, color) in enumerate(bars):
        offset = (i - 2.5) * width
        ax.bar(x + offset, values, width, label=label, color=color, edgecolor='black', linewidth=0.5)
    
    ax.set_title(title, fontweight='bold', pad=15)
    ax.set_ylabel('Execution Time (ms)')
    ax.set_xticks(x)
    ax.set_yscale('log')
    ax.set_xticklabels(data['formal_label'], rotation=40, ha='right')
    ax.grid(axis='y', linestyle='--')
    ax.legend(frameon=True, bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=9, ncol=1)
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {filename}")


create_6way_comparison(df_syn, 'Synthetic Workload Performance', 'synthetic_main_comparison.pdf')
create_6way_comparison(df_rw, 'Real World Workload Performance', 'real_world_main_comparison.pdf')


# ===== 2. 4-WAY GPU COMPARISON BAR GRAPHS =====
def create_4way_gpu_comparison(data, title, filename):
    """Create 4-way GPU comparison bar graph."""
    fig, ax = plt.subplots(figsize=(10, 5))
    
    x = np.arange(len(data))
    width = 0.2
    
    bars = [
        ('Heterogeneous', data['het_times'], color_set[0]),
        ('libcudf 25.10', data['libcudf'], color_set[1]),
        ('Warp per String', data['contains_warp'], color_set[2]),
        ('Thread per String', data['contains_thread'], color_set[3])
    ]
    
    for i, (label, values, color) in enumerate(bars):
        offset = (i - 1.5) * width
        ax.bar(x + offset, values, width, label=label, color=color, edgecolor='black', linewidth=0.5)
    
    ax.set_title(title, fontweight='bold', pad=15)
    ax.set_ylabel('Execution Time (ms)')
    ax.set_xticks(x)
    ax.set_xticklabels(data['formal_label'], rotation=40, ha='right')
    ax.grid(axis='y', linestyle='--')
    ax.legend(frameon=True, bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=9)
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {filename}")


create_4way_gpu_comparison(df_syn, 'Synthetic Workload Performance (GPU Implementations)', 'synthetic_gpu_comparison.pdf')
create_4way_gpu_comparison(df_rw, 'Real World Workload Performance (GPU Implementation)', 'real_world_gpu_comparison.pdf')


# ===== 3. STACKED BAR GRAPHS (BREAKDOWNS) =====
def create_breakdown_stacked(data, title, filename):
    """Create stacked bar graph showing breakdown of heterogeneous implementation."""
    fig, ax = plt.subplots(figsize=(9, 5))
    
    x = np.arange(len(data))
    width = 0.6
    
    # Stack the three breakdown components
    p1 = ax.bar(x, data['partition_breakdown'], width, label='Partitioning', 
                color=color_set[6], edgecolor='black', linewidth=0.5)
    p2 = ax.bar(x, data['thread_breakdown'], width, bottom=data['partition_breakdown'],
                label='Thread per String Execution', color=color_set[7], edgecolor='black', linewidth=0.5)
    p3 = ax.bar(x, data['warp_breakdown'], width, 
                bottom=data['partition_breakdown'] + data['thread_breakdown'],
                label='Warp per String Execution', color=color_set[8], edgecolor='black', linewidth=0.5)
    
    ax.set_title(title, fontweight='bold', pad=15)
    ax.set_ylabel('Execution Time (ms)')
    ax.set_xticks(x)
    ax.set_xticklabels(data['formal_label'], rotation=40, ha='right')
    ax.grid(axis='y', linestyle='--')
    ax.legend(frameon=True, bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=9)
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {filename}")


create_breakdown_stacked(df_syn, 'Heterogeneous Implementation Breakdown: Synthetic', 'synthetic_breakdown.pdf')
create_breakdown_stacked(df_rw, 'Heterogeneous Implementation Breakdown: Real World', 'real_world_breakdown.pdf')


# ===== 4. BREAKDOWN COMPARISON (STACKED vs LIBCUDF) =====
def create_breakdown_comparison(data, title, filename):
    """Create comparison between stacked heterogeneous breakdown and libcudf."""
    fig, ax = plt.subplots(figsize=(10, 5))
    
    x = np.arange(len(data))
    width = 0.35
    
    # Heterogeneous stacked bars (left)
    p1 = ax.bar(x - width/2, data['partition_breakdown'], width, label='Partitioning',
                color=color_set[6], edgecolor='black', linewidth=0.5)
    p2 = ax.bar(x - width/2, data['thread_breakdown'], width, bottom=data['partition_breakdown'],
                label='Thread per String Execution', color=color_set[7], edgecolor='black', linewidth=0.5)
    p3 = ax.bar(x - width/2, data['warp_breakdown'], width,
                bottom=data['partition_breakdown'] + data['thread_breakdown'],
                label='Warp per String Execution', color=color_set[8], edgecolor='black', linewidth=0.5)
    
    # libcudf bars (right)
    p4 = ax.bar(x + width/2, data['libcudf'], width, label='libcudf 25.10',
                color=color_set[1], edgecolor='black', linewidth=0.5)
    
    ax.set_title(title, fontweight='bold', pad=15)
    ax.set_ylabel('Execution Time (ms)')
    ax.set_xticks(x)
    ax.set_xticklabels(data['formal_label'], rotation=40, ha='right')
    ax.grid(axis='y', linestyle='--')
    ax.legend(frameon=True, bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=8, ncol=1)
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {filename}")


create_breakdown_comparison(df_syn, 'Synthetic Workload Breakdown', 'synthetic_breakdown_comparison.pdf')
create_breakdown_comparison(df_rw, 'Real World Workload Breakdown', 'real_world_breakdown_comparison.pdf')


# ===== 5. SPEEDUP OVER LIBCUDF (COMBINED WORKLOADS) =====
def create_speedup_graph():
    """Create speedup comparison over libcudf for all workloads."""
    # Calculate speedup for each workload
    df['speedup'] = df['libcudf'] / df['het_times']
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    x = np.arange(len(df))
    width = 0.6
    
    # Color synthetic workloads differently from Real World
    colors_list = [color_set[0] if i < fb_idx else color_set[9] for i in range(len(df))]
    
    bars = ax.bar(x, df['speedup'], width, color=colors_list, edgecolor='black', linewidth=0.5)
    
    # Add horizontal line at speedup = 1.0
    ax.axhline(y=1.0, color='gray', linestyle='--', linewidth=1.5, label='No Speedup (1.0×)')
    
    ax.set_title('Speedup over libcudf 25.10 (All Workloads)', fontweight='bold', pad=15)
    ax.set_ylabel('Speedup (×)')
    ax.set_xlabel('Workload')
    ax.set_xticks(x)
    ax.set_xticklabels(df['formal_label'], rotation=40, ha='right')
    ax.grid(axis='y', linestyle='--')
    
    # Custom legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=color_set[0], edgecolor='black', label='Synthetic'),
        Patch(facecolor=color_set[9], edgecolor='black', label='Real World'),
        plt.Line2D([0], [0], color='gray', linestyle='--', linewidth=1.5, label='No Speedup (1.0×)')
    ]
    ax.legend(handles=legend_elements, frameon=True, loc='upper left', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('speedup.pdf', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: speedup.pdf")


create_speedup_graph()

print("\n✓ All plots generated successfully!")
print("Generated files:")
print("  - synthetic_main_comparison.pdf")
print("  - real_world_main_comparison.pdf")
print("  - synthetic_gpu_comparison.pdf")
print("  - real_world_gpu_comparison.pdf")
print("  - synthetic_breakdown.pdf")
print("  - real_world_breakdown.pdf")
print("  - synthetic_breakdown_comparison.pdf")
print("  - real_world_breakdown_comparison.pdf")
print("  - speedup.pdf")